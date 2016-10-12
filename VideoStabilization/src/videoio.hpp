/*
 * =====================================================================================
 *
 *       Filename:  videoio.hpp
 *
 *    Description:  Read video files into opencv format.
 *
 *        Version:  1.0
 *        Created:  10/12/2016 01:25:38 PM
 *       Revision:  none
 *       Compiler:  gcc
 *
 *         Author:  Dilawar Singh (), dilawars@ncbs.res.in
 *   Organization:  NCBS Bangalore
 *
 * =====================================================================================
 */


#ifndef  videoio_INC
#define  videoio_INC

#include <tiffio.h>
#include <opencv2/videoio.hpp>
#include <opencv2/opencv.hpp>

using namespace std;
using namespace cv;

typedef struct VideoInfo 
{
    size_t width = 0;
    size_t height = 0;
    float fps = 0;
    size_t numFrames = 0;
} video_info_t;


/**
 * @brief  Read data from TIFF images are vector of opencv matrix.
 *
 * @tparam pixal_type_t
 * @param 
 * @param 
 * @param 
 */
template< typename pixal_type_t >
void get_frames_from_tiff( const string& filename
        , vector< Mat_< pixal_type_t > >& frames 
        , video_info_t& vidInfo
        )
{
    TIFF *tif = TIFFOpen( filename.c_str(), "r");
    if (tif) {
        int dircount = 0;
        do 
        {
            dircount++;
            uint32 w, h;

            TIFFGetField( tif, TIFFTAG_IMAGEWIDTH, &w);
            TIFFGetField( tif, TIFFTAG_IMAGELENGTH, &h);
            size_t npixals = w * h;

            uint32* raster;
            raster = ( uint32* ) _TIFFmalloc( npixals * sizeof( uint32 ));
            if( NULL != raster )
            {
                if( TIFFReadRGBAImage( tif, w, h, raster, 0 ) )
                {
                    vidInfo.width = w;
                    vidInfo.height = h;
                    vidInfo.numFrames += 1;
                    Mat image(h, w, CV_8U, raster );
                    frames.push_back( image );
                }
            }
            _TIFFfree( raster );
        } while (TIFFReadDirectory(tif));
    }
    cout << "[INFO] Read " << frames.size() << " frames from "
        << filename << endl;
    TIFFClose(tif);
}

template< typename pixal_type_t >
void get_frames_from_avi( const string& filename
        , vector< Mat_< pixal_type_t > >& frames 
        , video_info_t& vidInfo
        )
{
    VideoCapture inputVideo( filename.c_str() );

    if(! inputVideo.isOpened())
    {
        std::cout << "Could not open " << filename << std::endl;
        return;
    }

    Mat cur, curGrey;

    vidInfo.width = (int) inputVideo.get(CV_CAP_PROP_FRAME_WIDTH);
    vidInfo.height = (int) inputVideo.get(CV_CAP_PROP_FRAME_HEIGHT);

    while(true) 
    {
        inputVideo >> cur;
        if(cur.data == NULL) {
            break;
        }
        cvtColor(cur, curGrey, COLOR_BGR2GRAY);
        frames.push_back( curGrey );
        vidInfo.numFrames += 1;
    }

    inputVideo.release( );
    cout << "[INFO] Read " << frames.size() << " frames from "
        << filename << endl;
}

template< typename pixal_type_t >
void read_frames( const string& filename
        , vector< Mat_<pixal_type_t> >& frames 
        , video_info_t& vidInfo
        )
{

    string::size_type pAt = filename.find_last_of('.');       
    string ext = filename.substr( pAt+1 );
    std::cout << "[INFO] Extenstion of file " << ext << std::endl;

    Size frameSize;
    size_t fps = 15;

    if( ext == "tif" || ext == "tiff" )
    {
        std::cout << "[INFO] Got a tiff file" << std::endl;
        get_frames_from_tiff<pixal_type_t>( filename, frames, vidInfo );
    }
    else if( ext == "avi" )
    {
        std::cout << "[INFO] Got a avi file" << std::endl;
        get_frames_from_avi<pixal_type_t>( filename, frames, vidInfo );
    }

}


#endif   /* ----- #ifndef videoio_INC  ----- */
