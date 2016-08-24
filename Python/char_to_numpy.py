"""char_to_numpy.py: 

Generates a numpy array out of a character.

"""
    
__author__           = "Dilawar Singh"
__copyright__        = "Copyright 2016, Dilawar Singh"
__credits__          = ["NCBS Bangalore"]
__license__          = "GNU GPL"
__version__          = "1.0.0"
__maintainer__       = "Dilawar Singh"
__email__            = "dilawars@ncbs.res.in"
__status__           = "Development"

import sys
import os
import matplotlib.pyplot as plt
import numpy as np

def conevert( char, size = 20 ):
    fig = plt.figure(  )
    ax = fig.add_subplot( 111 )
    plt.axis( 'off' )
    ax.text( 0.5, 0.5, char, fontsize = 144 )
    fig.canvas.draw()
    data = np.fromstring( fig.canvas.tostring_rgb(), dtype=np.uint8 )
    l, b, w, h = fig.bbox.bounds
    w, h = int(w), int(h)
    data.shape = h, w, 3
    plt.close()
    plt.figure()
    plt.imshow( data )
    plt.show()


def main( ):
    char = sys.argv[1]
    print( 'Converting %s' % char )
    conevert( char )

if __name__ == '__main__':
    main()

