#!/usr/bin/env python3

"""estimator.py: 

Estimate.
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


mean_, std_ = 0, 0

y1, y2 = [ ], [ ]
y1err, y2err = [ ], [ ]

def estimate( i, s ):
    global mean_, std_
    m, u = np.mean( s ), np.std( s )
    y1.append( m )
    y2.append( u )
    y1err.append( abs(m) )
    y2err.append( abs(u - 1.0) )


def main( ):
    global y1, y2, y1err, y2err
    samples = np.random.normal( 0, 1, 2000 )
    meanVec = [ ]
    for i, s in enumerate(samples[3:]):
        estimate( i, samples[:i+3] )

    plt.plot( y1err, '-o', label = 'Err(mean)' )
    plt.plot( y2err, '-o', label = 'Err(var)' )
    plt.legend(loc='best', framealpha=0.4)
    plt.savefig( '%s.png' % sys.argv[0] )


if __name__ == '__main__':
    main()

