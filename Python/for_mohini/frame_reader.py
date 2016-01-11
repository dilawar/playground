"""image_reader.py: 

    Extract frames from input file.

"""
    
__author__           = "Dilawar Singh"
__copyright__        = "Copyright 2015, Dilawar Singh and NCBS Bangalore"
__credits__          = ["NCBS Bangalore"]
__license__          = "GNU GPL"
__version__          = "1.0.0"
__maintainer__       = "Dilawar Singh"
__email__            = "dilawars@ncbs.res.in"
__status__           = "Development"

import numpy as np
import cv2

import logging 
logger = logging.getLogger('')

def get_frame_data( frame ):
    try:
        img = np.array(frame)
    except Exception as e:
        img = np.array(frame.convert('L'))
    return to_grayscale(img)

def to_grayscale( img ):
    if len(img.shape) == 3:
        img = np.dot( img[...,:3], [ 0.299, 0.587, 0.114 ] )

    if img.max() >= 256.0:
        logging.debug("Converting image to grayscale")
        logging.debug("Max=%s, min=%s, std=%s"% (img.max(), img.min(),
            img.std()))
        img = 255 * ( img / float( img.max() ))
    gimg = np.array(img, dtype=np.uint8)
    return gimg

def read_frames_from_avi( filename, max_frames = None ):
    cap = cv2.VideoCapture( filename )
    i, frames = 0, []
    while cap.isOpened():
        try:
            ret, frame = cap.read()
        except Exception as e:
            print("Failed to read frame. Error %s" % e)
            quit()
        if ret:
            gray = cv2.cvtColor( frame, cv2.COLOR_BGR2GRAY)
            i += 1
            frames.append( gray )
            if i == max_frames:
                break

    logger.info("Total %s frames read" % len(frames))
    return frames


def read_frames_from_tiff( filename, max_frames = -1 ):
    from PIL import Image
    tiff = Image.open( filename )
    i, frames = 0, []
    try:
        while 1:
            i += 1
            tiff.seek( tiff.tell() + 1 )
            framedata = get_frame_data( tiff )
            frames.append( framedata )
            if max_frames == i:
                break
    except EOFError as e:
        pass

    logger.info("Total frames: %s" % len(frames) )
    return frames

def read_frames( videofile, max_frames = -1):
    ext = videofile.split('.')[-1]
    if ext in [ 'tif', 'tiff' ]:
        return read_frames_from_tiff( videofile, max_frames )
    elif ext in [ 'avi', 'mp4' ]:
        return read_frames_from_avi ( videofile, max_frames )
    else:
        logger.error('Format %s is not supported yet' % ext )
        quit()
