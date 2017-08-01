"""frames.py: 
Frames

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
import sympy

def main( ):
    l = 10
    n = 15
    frame = np.random.randint( 0, 2, size=(n, l) )
    print( frame )
    y = np.dot( frame, np.dot( frame.T, frame ) ^ -1 )
    print( y )

    quit( )
    for i in range( 10 ):
        y = np.random.randint( 0, 100, n )
        p = np.linalg.norm( np.dot( frame.T,  y ), 2 )
        x = np.linalg.norm( y )
        print( p, x )

if __name__ == '__main__':
    main()
