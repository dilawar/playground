"""compressed_sensing.py: 

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
from pyCSalgos.BP.l1eq_pd import l1eq_pd

N = 256
P = 5
K = 64
x = np.zeros( N )

def sparse_signal( ):
    x[5] = 1
    x[20] = 2.0
    x[100] = 11
    x[151] = -5
    x[180 ] = 3
    return x

def obtain_random_measurements( x, k):
    A = np.random.randn( k, N )
    return A, np.dot( A, x )

def main( ):
    gridSize = (3, 1)
    ax1 = plt.subplot2grid( gridSize, (0,0), colspan = 1 )
    ax2 = plt.subplot2grid( gridSize, (1,0), colspan = 1 )
    ax3 = plt.subplot2grid( gridSize, (2,0), colspan = 1 )

    # Make a sparse singal.
    x = sparse_signal( )
    ax1.plot( x, label = 'sparse signal' )
    ax1.legend(loc='best', framealpha=0.4)

    A, y = obtain_random_measurements( x, K )
    ax2.plot( y, label = 'measurements' )
    ax2.legend(loc='best', framealpha=0.4)

    # compressed recovery.
    x0 = np.dot( A.T,  y )
    res = l1eq_pd( x0, A, [ ], y )
    print( 'Error:', np.linalg.norm( res - x0 ) )
    ax3.plot( res, label = 'reconstructed' )
    ax3.legend(loc='best', framealpha=0.4)

    plt.title( 'Compressed sensing' )
    plt.savefig( 'compressed_sensing.png' )


if __name__ == '__main__':
    main()
