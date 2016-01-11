#!/usr/bin/env python

"""video_activitity_merger.py: 

Given a video file and a activity file, creates an animation.

"""
    
__author__           = "Dilawar Singh"
__copyright__        = "Copyright 2015, Dilawar Singh and NCBS Bangalore"
__credits__          = ["NCBS Bangalore"]
__license__          = "GNU GPL"
__version__          = "1.0.0"
__maintainer__       = "Dilawar Singh"
__email__            = "dilawars@ncbs.res.in"
__status__           = "Development"

import cv2
import numpy as np
import matplotlib 
import matplotlib.pyplot as plt
import matplotlib.animation as anim
import sys
import os 
import scipy.io
import frame_reader as fr

data_ = None
cap_ = None
fig_ = plt.figure()
fig_.patch.set_facecolor('black')
fps_ = 0.0

ax1 = fig_.add_subplot(2, 1, 1)
ax1.set_title('Motor recording', color='white')
ax1.set_xlabel('Time (sec)', color = 'white')
ax1.tick_params(axis='x', colors='white')
ax2 = fig_.add_subplot(2, 1, 2)
ax2.set_title('Purkinje cells', color='white')
ax2.tick_params(axis='x', colors='white')
# Inset for raw data.
save_video_ = True
writer_ = None

axes_ = { 'video' : ax2, 'activity' : ax1 }
lines_ = {}
lines_["video"] = ax2.imshow( np.zeros((100,100)), vmax=255, cmap = plt.gray(), animated = True)
lines_['activity'] = ax1.plot([], [], color = 'blue')[0]

time_template_ = 'Time = %.1f s'
time_text_ = fig_.text(0.05, 0.9, '', transform=axes_['video'].transAxes)

t_ = []
y_ = []
args_ = None
stride_ = None


def init():
    global axes_, lines_
    global cap_, args_
    global data_
    global frames_
    global stride_
    global t_, y_
    global fps_

    videoFile = args_['video']
    frames_ = fr.read_frames( videoFile )
    data_ = scipy.io.loadmat( args_['activity'] )
    data_ = data_['final']
    t_, y_ = data_[:,0], data_[:,1]
    fps_ =  args_['fps']
    tmax = len(frames_) / float(fps_)
    stride_ = len(y_) / len(frames_)
    print('[INFO] Total frames: %s' % len(frames_))
    print('[INFO] Computed fps: %s' % fps_)
    print('[INFO] Stride to take: %s' % stride_)
    axes_['activity'].set_xlim([0, tmax])
    axes_['activity'].set_ylim([y_.min() - 2, y_.max() + 2])
    return lines_.values()

def update_axis_limits(ax, x, y):
    xlim = ax.get_xlim()
    if x >= xlim[1]:
        ax.set_xlim(xlim[0], x+10)

    ylims = ax.get_ylim()
    if y >= ylims[1]:
        ax.set_ylim(ylims[0], y+1)

def animate(i):
    global y_
    global frames_ 
    global time_text_
    global box_
    global tvec_, y1_, y2_
    global cap_
    global fig_ax_
    global stride_
    global fps_

    if i >= len(frames_):
        print('[INFO] All done')
        quit()

    lines_['video'].set_array( frames_[i] )
    start, stop = int((i-5)*stride_), int(i * stride_)
    y = y_[:stop]
    lines_['activity'].set_data( np.arange(len(y)) / float(stride_ * fps_), y)
    return lines_.values(), time_text_

def animate_together( ):
    global ani_, cap_
    global save_video_
    global args_
    global frames_
    nframes = 180
    ani_ = anim.FuncAnimation(
            fig_
            , animate
            , frames = nframes
            , interval = 25
            , init_func=init
            , blit = False
            )

    if save_video_:
        print("Writing to video file output.mp4")
        ani_.save('output.mp4', fps=args_['fps']) #, extra_args=['-vcodec', 'libx264'])
    plt.show( )

def main( **kwargs ):
    global data_, args_
    vidFile = args_['video']
    if not os.path.exists(vidFile):
        print("[WARN] Given file %s does not exits" % vidFile)
        quit()
    try:
        animate_together()
    except Exception as e:
        print('[ERR] failed to animate: %s' % e)

if __name__ == '__main__':

    import argparse
    # Argument parser.
    description = '''Video and activity file merger. Plot animation.'''
    parser = argparse.ArgumentParser(description=description)
    parser.add_argument('--video', '-v'
        , required = True
        , help = 'Input video file'
        )
    parser.add_argument('--activity', '-a'
        , required = False
        , help = 'Activity file'
        )
    parser.add_argument( '--fps', '-f'
        , required = True
        , default = 1
        , type = int
        , help = 'How long is the video?'
        )
    class Args: pass 
    args = Args()
    parser.parse_args(namespace=args)
    args_ = vars( args )
    main( )
