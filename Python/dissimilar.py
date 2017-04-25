"""dissimilar.py: 

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
import itertools
import numpy as np

def prefix( char, string ):
    loc = string.find( char )

def computeIndex( x, ref ):
    index = 0.0
    print( 'Computing index of %s' % x )
    y = ''
    x = x 
    print( 'Test string is %s' % x )
    for i, c in enumerate(x):
        if i == 0:
            start = -1
        else:
            start = ref.find( x[i-1] )
        end = ref.find( c )
        if start > end:
            start = -1
        y += ref[start+1: end] + c

    index = float( len( y ) ) / len( ref )
    return index


def main( teststring ):
    allPermulations = itertools.permutations( teststring )
    yvec = [ ]
    xvec = [ ]
    result = [ ]
    for x in allPermulations:
        x = "".join( x )
        index = computeIndex( x, teststring )
        yvec.append( index )
        xvec.append( x )
        result.append( (index, x) )

    result = sorted( result )
    yvec, xvec = zip( *result )

    plt.plot( 1.0 / np.array( yvec ) )
    plt.xticks( range(len(xvec)), xvec
            , rotation = 'vertical'
            , fontsize = 6 )
    plt.tight_layout( )
    plt.savefig( '%s.png' % sys.argv[0] )

if __name__ == '__main__':
    main( 'ABCD' )
