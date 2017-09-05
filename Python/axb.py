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

def sparse_vec( n, p = 0.05 ):
    return np.random.choice( [0,1], n, [p, 1-p ] )

def main( ):
    imgs = [ ]
    for i in range( 10000 ):
        print( 'Loop %d' % i )
        s = sparse_vec( 100 )
        ss = s[:]
        np.random.shuffle( ss )
        ss = np.matrix( ss )

        sa = np.matrix( s )
        si = np.linalg.pinv( np.matrix( s ) )
        a =  ss.T * si.T 
        imgs.append( a )

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

if __name__ == '__main__':
    main()
