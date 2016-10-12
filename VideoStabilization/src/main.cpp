/*
Copyright (c) 2014, Nghia Ho
Copyright (c) 2016 -, Dilawar Singh  <dilawars@ncbs.res.in>

All rights reserved.

Redistribution and use in source and binary forms, with or without modification,
are permitted provided that the following conditions are met:

1. Redistributions of source code must retain the above copyright notice, this
list of conditions and the following disclaimer.

2. Redistributions in binary form must reproduce the above copyright notice,
this list of conditions and the following disclaimer in the documentation and/or
other materials provided with the distribution.

3. Neither the name of the copyright holder nor the names of its contributors
may be used to endorse or promote products derived from this software without
specific prior written permission.

THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS" AND
ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED
WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE
DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT HOLDER OR CONTRIBUTORS BE LIABLE FOR
ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES
(INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES;
LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON
ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT
(INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE OF THIS
SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.

--------------------------------------------------------------------------------
Modification log:

    Wed 12 Oct 2016 10:59:23 AM IST , Dilawar Singh
        - Compiled with opencv-3 on openSUSE-Tumbleweed.
        - Added CMake support.
        - Added tiff support.
        - 
*/
 
#include <opencv2/videoio.hpp>
#include <opencv2/opencv.hpp>
#include <iostream>
#include <cassert>
#include <cmath>
#include <fstream>
#include <tiffio.h>

using namespace std;
using namespace cv;

typedef unsigned char pixal_type_t;
typedef Mat matrix_type_t;

// This video stablisation smooths the global trajectory using a sliding average window
const int SMOOTHING_RADIUS = 30; // In frames. The larger the more stable the video, but less reactive to sudden panning
const int HORIZONTAL_BORDER_CROP = 20; // In pixels. Crops the border to reduce the black borders from stabilisation being too noticeable.

// 1. Get previous to current frame transformation (dx, dy, da) for all frames
// 2. Accumulate the transformations to get the image trajectory
// 3. Smooth out the trajectory using an averaging window
// 4. Generate new set of previous to current transform, such that the trajectory ends up being the same as the smoothed trajectory
// 5. Apply the new transformation to the video

struct TransformParam
{
    TransformParam() {}
    TransformParam(double _dx, double _dy, double _da) {
        dx = _dx;
        dy = _dy;
        da = _da;
    }

    double dx;
    double dy;
    double da; // angle
};

struct Trajectory
{
    Trajectory() {}
    Trajectory(double _x, double _y, double _a) {
        x = _x;
        y = _y;
        a = _a;
    }

    double x;
    double y;
    double a; // angle
};

struct VideoInfo 
{
    size_t width;
    size_t height;
    float fps;
    size_t numFrames;
};

VideoInfo vidInfo_;

Size get_data_from_tifffile( const string filename, vector<matrix_type_t>& frames )
{
    TIFF *tif = TIFFOpen( filename.c_str(), "r");
    long sls = TIFFScanlineSize( tif );
    void* raster;
    raster = _TIFFmalloc( sls );

    Size s;

    if (tif) {
	int dircount = 0;
        // Iterate over each frame now.
	do 
        {
	    dircount++;
            uint32 w, h;
            size_t npixals;

            TIFFGetField( tif, TIFFTAG_IMAGEWIDTH, &w);
            TIFFGetField( tif, TIFFTAG_IMAGELENGTH, &h);
            npixals = w * h;

            s.width = w;
            s.height = h;


            // Unsigned values in tiff.
            matrix_type_t image(1, npixals, CV_16U );
            pixal_type_t* scanline;

            for (size_t i = 0; i < h; i++) 
            {
                TIFFReadScanline( tif, raster, i, 0 );
                scanline = image.ptr(i);
                memcpy(raster, scanline, sls);
            }
            frames.push_back( image );

	} while (TIFFReadDirectory(tif));
    }
    printf( "[INFO] Done reading %d images from %s\n"
            , frames.size(), filename.c_str() 
            );
    TIFFClose(tif);
    return s;
}

void write_to_video( VideoWriter& vid, const Mat&  frame )
{
    try {
        vid.write( frame );
    }
    catch( exception e )
    {
        std::cout << "Failed to write this frame" << std::endl;
    }
}

Size get_data_from_avi( const string filename, vector< matrix_type_t >& frames)
{
    VideoCapture inputVideo( filename.c_str() );
    assert(inputVideo.isOpened());
    Mat cur, curGrey;
    while(true) 
    {
        inputVideo >> cur;
        if(cur.data == NULL) {
            break;
        }
        cvtColor(cur, curGrey, COLOR_BGR2GRAY);
        frames.push_back( curGrey );
    }
    Size S = Size((int) inputVideo.get(CV_CAP_PROP_FRAME_WIDTH),    // Acquire input size
            (int) inputVideo.get(CV_CAP_PROP_FRAME_HEIGHT));
    return S;
}

int main(int argc, char **argv)
{
    if(argc < 3) {
        cout << "./videostab input_file output_file" << endl;
        return 0;
    }

    // For further analysis
    ofstream out_transform("prev_to_cur_transformation.txt");
    ofstream out_trajectory("trajectory.txt");
    ofstream out_smoothed_trajectory("smoothed_trajectory.txt");
    ofstream out_new_transform("new_prev_to_cur_transformation.txt");


    // Step 0. Prepare output file.
    string source( argv[1] );                   /* Input file */

    string::size_type pAt = source.find_last_of('.');       
    string ext = source.substr( pAt+1 );
    std::cout << "[INFO] Extenstion of file " << ext << std::endl;

    vector< matrix_type_t > frames;

    Size frameSize;
    size_t fps = 15;

    if( ext == "tif" || ext == "tiff" )
    {
        std::cout << "[INFO] Got a tiff file" << std::endl;
        frameSize = get_data_from_tifffile( source, frames );
    }
    else if( ext == "avi" )
    {
        std::cout << "[INFO] Got a avi file" << std::endl;
        frameSize = get_data_from_avi( source, frames );
    }

    const string outfileName = argv[2];


    VideoWriter outputVideo;                                        // Open the output

    // Write both video onto canvas. Good for debugging.
    VideoWriter canvasVideo;

    outputVideo.open(outfileName, CV_FOURCC('D', 'I', 'V', 'X'), fps, frameSize, true);

    Size canvasSize = Size( 2*frameSize.width+10, frameSize.height);
    canvasVideo.open("canvas.avi", CV_FOURCC( 'D', 'I', 'V', 'X' ), fps, canvasSize, true);

    if (!outputVideo.isOpened())
    {
        cout  << "Could not open the output video for write: " << outfileName << endl;
        return -1;
    }

    // Step 1 - Get previous to current frame transformation (dx, dy, da) for all frames
    vector <TransformParam> prev_to_cur_transform; // previous to current

    int k=1;
    Mat last_T;
    Mat curGrey, prevGrey;
    for (size_t i = 1; i < frames.size(); i++) 
    {
        prevGrey = frames[i-1];
        curGrey = frames[i];
        // vector from prev to cur
        vector <Point2f> prev_corner, cur_corner;
        vector <Point2f> prev_corner2, cur_corner2;
        vector <uchar> status;
        vector <float> err;

        goodFeaturesToTrack(prevGrey, prev_corner, 200, 0.01, 30);
        calcOpticalFlowPyrLK(prevGrey, curGrey, prev_corner, cur_corner, status, err);

        // weed out bad matches
        for(size_t i=0; i < status.size(); i++) {
            if(status[i]) {
                prev_corner2.push_back(prev_corner[i]);
                cur_corner2.push_back(cur_corner[i]);
            }
        }

        // translation + rotation only
        Mat T = estimateRigidTransform(prev_corner2, cur_corner2, false); // false = rigid transform, no scaling/shearing

        // in rare cases no transform is found. We'll just use the last known good transform.
        if(T.data == NULL) {
            last_T.copyTo(T);
        }

        T.copyTo(last_T);

        // decompose T
        double dx = T.at<double>(0,2);
        double dy = T.at<double>(1,2);
        double da = atan2(T.at<double>(1,0), T.at<double>(0,0));

        prev_to_cur_transform.push_back(TransformParam(dx, dy, da));

        out_transform << k << " " << dx << " " << dy << " " << da << endl;

        curGrey.copyTo(prevGrey);

        cout << "Frame: " << k << "/" << frames.size() << " - good optical flow: " << prev_corner2.size() << endl;
        k++;
    }

    // Step 2 - Accumulate the transformations to get the image trajectory

    // Accumulated frame to frame transform
    double a = 0;
    double x = 0;
    double y = 0;

    vector <Trajectory> trajectory; // trajectory at all frames

    for(size_t i=0; i < prev_to_cur_transform.size(); i++) 
    {
        x += prev_to_cur_transform[i].dx;
        y += prev_to_cur_transform[i].dy;
        a += prev_to_cur_transform[i].da;

        trajectory.push_back(Trajectory(x,y,a));

        out_trajectory << (i+1) << " " << x << " " << y << " " << a << endl;
    }

    // Step 3 - Smooth out the trajectory using an averaging window
    vector <Trajectory> smoothed_trajectory; // trajectory at all frames

    for(size_t i=0; i < trajectory.size(); i++) {
        double sum_x = 0;
        double sum_y = 0;
        double sum_a = 0;
        int count = 0;

        for(int j=-SMOOTHING_RADIUS; j <= SMOOTHING_RADIUS; j++) {
            if(i+j >= 0 && i+j < trajectory.size()) {
                sum_x += trajectory[i+j].x;
                sum_y += trajectory[i+j].y;
                sum_a += trajectory[i+j].a;

                count++;
            }
        }

        double avg_a = sum_a / count;
        double avg_x = sum_x / count;
        double avg_y = sum_y / count;

        smoothed_trajectory.push_back(Trajectory(avg_x, avg_y, avg_a));

        out_smoothed_trajectory << (i+1) << " " << avg_x << " " << avg_y << " " << avg_a << endl;
    }

    // Step 4 - Generate new set of previous to current transform, such that the trajectory ends up being the same as the smoothed trajectory
    vector <TransformParam> new_prev_to_cur_transform;

    // Accumulated frame to frame transform
    a = 0;
    x = 0;
    y = 0;

    for(size_t i=0; i < prev_to_cur_transform.size(); i++) {
        x += prev_to_cur_transform[i].dx;
        y += prev_to_cur_transform[i].dy;
        a += prev_to_cur_transform[i].da;

        // target - current
        double diff_x = smoothed_trajectory[i].x - x;
        double diff_y = smoothed_trajectory[i].y - y;
        double diff_a = smoothed_trajectory[i].a - a;

        double dx = prev_to_cur_transform[i].dx + diff_x;
        double dy = prev_to_cur_transform[i].dy + diff_y;
        double da = prev_to_cur_transform[i].da + diff_a;

        new_prev_to_cur_transform.push_back(TransformParam(dx, dy, da));

        out_new_transform << (i+1) << " " << dx << " " << dy << " " << da << endl;
    }

    // Step 5 - Apply the new transformation to the video
    //inputVideo.set(CV_CAP_PROP_POS_FRAMES, 0);
    Mat T(2,3,CV_64F);

    // get the aspect ratio correct
    int vert_border = HORIZONTAL_BORDER_CROP * prevGrey.rows / prevGrey.cols; 

    for( size_t k = 0; k < frames.size() -1; k ++ )
    { 
        // don't process the very last frame, no valid transform
        curGrey = frames[0];

        T.at<double>(0,0) = cos(new_prev_to_cur_transform[k].da);
        T.at<double>(0,1) = -sin(new_prev_to_cur_transform[k].da);
        T.at<double>(1,0) = sin(new_prev_to_cur_transform[k].da);
        T.at<double>(1,1) = cos(new_prev_to_cur_transform[k].da);

        T.at<double>(0,2) = new_prev_to_cur_transform[k].dx;
        T.at<double>(1,2) = new_prev_to_cur_transform[k].dy;

        Mat cur2;

        warpAffine(curGrey, cur2, T, curGrey.size());

        cur2 = cur2(Range(vert_border, cur2.rows-vert_border), Range(HORIZONTAL_BORDER_CROP, cur2.cols-HORIZONTAL_BORDER_CROP));

        // Resize cur2 back to cur size, for better side by side comparison
        resize(cur2, cur2, curGrey.size());

        // Now draw the original and stablised side by side for coolness
        Mat canvas = Mat::zeros(curGrey.rows, curGrey.cols*2+10, curGrey.type());

        curGrey.copyTo(canvas(Range::all(), Range(0, cur2.cols)));
        cur2.copyTo(canvas(Range::all(), Range(cur2.cols+10, cur2.cols*2+10)));

#if 1
        // If too big to fit on the screen, then scale it down by 2, hopefully it'll fit :)
        if(canvas.cols > 1920) {
            resize(canvas, canvas, Size(canvas.cols/2, canvas.rows/2));
        }
#endif

        write_to_video( outputVideo, cur2 );

        assert( canvas.rows == canvasSize.height );
        assert( canvas.cols == canvasSize.width );
        write_to_video( canvasVideo, canvas);
    }

    outputVideo.release( );
    canvasVideo.release( );

    std::cout << "Wrote modified video to " << outfileName << std::endl;
    std::cout << "Wrote input and modified video to canvas.avi" << std::endl;

    return 0;
}
