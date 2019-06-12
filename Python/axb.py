"""axb.py: 

"""
    
__author__           = "Dilawar Singh"
__copyright__        = "Copyright 2017-, Dilawar Singh"
__version__          = "1.0.0"
__maintainer__       = "Dilawar Singh"
__email__            = "dilawars@ncbs.res.in"
__status__           = "Development"

import sys
import os
import matplotlib.pyplot as plt
import numpy as np
import random

if not os.path.exists( '_figures' ):
    os.makedirs( '_figures' )

def sparse_vec( n, p = 0.05 ):
    return np.random.choice( [0,1], n, [p, 1-p ] )

def main( ):
    iterations = 10000
    N = 100
    plot = False
    imgs = np.ndarray( shape=(iterations, N, N) )
    for i in range( iterations ):
        s = sparse_vec( N )
        ss = s[:]
        np.random.shuffle( ss )
        err = 1.0
        ss = np.matrix( ss + err )

        sa = np.matrix( s )
        si = np.linalg.pinv( np.matrix( s ) )
        a =  ss.T * si.T 
        imgs[i] = a
        if plot:
            plt.imshow( a, interpolation = 'none', aspect = 'auto' )
            plt.colorbar( )
            plt.savefig( './_figures/fig%04d.png' % i )
            plt.close( )

    plt.figure( )
    avgImg = np.mean( imgs, axis = 0 ) 
    sumImg = np.sum( imgs, axis = 0 )
    varImg = np.std( imgs, axis = 0 )

    plt.subplot( 121 )
    plt.imshow( avgImg, aspect = 'auto', interpolation = 'none' )
    plt.colorbar( )
    plt.subplot( 122 )
    plt.imshow( varImg, aspect = 'auto', interpolation = 'none' )
    plt.colorbar( )
    plt.savefig( '%s.png' % sys.argv[0] )

    # Now use avgImg to compute the RIP.
    ds = [ ]
    for i in range( 1000 ):
        x = sparse_vec( N )
        a = varImg
        y = a.dot( x )
        assert x.shape == y.shape
        ds.append( np.linalg.norm( y ) / np.linalg.norm( x ) )
    print( np.mean( ds ), np.std( ds ), np.max( ds ), np.min( ds ) )

if __name__ == '__main__':
    main()
