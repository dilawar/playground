"""raster_interpolate.py: 

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
import scipy.interpolate

def main( ):
    x = [1, 25, 23, 4, 29, 15 ]
    y = [ 11, 23, 32, 21, 5, 15 ]
    f = [ 12, 12, 32, -8, -11, 20 ]
    rbfi = scipy.interpolate.Rbf( x, y, f )
    N = 33
    baseImg = np.zeros( shape = (N, N ) )
    for k, (i, j) in enumerate( zip( x, y ) ):
        baseImg[ i, j ] = f[k]

    print( baseImg )
    img = [ ]
    for i in range( N ):
        xi = [ i ] * N
        yi = range( N )
        fi = rbfi( xi, yi )
        img.append( fi )
    plt.subplot( 2, 1, 1 )
    plt.imshow( baseImg, interpolation = 'none' )
    plt.colorbar( )

    plt.subplot( 2, 1, 2 )
    plt.imshow( img, interpolation = 'none' )
    plt.colorbar( )
    plt.show( )

if __name__ == '__main__':
    main()
