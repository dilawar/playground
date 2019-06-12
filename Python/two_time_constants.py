"""test_decay.py: 

If two timecourse are mixed, how the decay profile looks like.

"""
    
__author__           = "Dilawar Singh"
__copyright__        = "Copyright 2017-, Dilawar Singh"
__version__          = "1.0.0"
__maintainer__       = "Dilawar Singh"
__email__            = "dilawars@ncbs.res.in"
__status__           = "Development"

import sys
import os
import random
import numpy as np

import matplotlib as mpl
import matplotlib.pyplot as plt
mpl.style.use( 'bmh' )
mpl.rcParams['axes.linewidth'] = 0.2
mpl.rcParams['lines.linewidth'] = 1.0
mpl.rcParams['text.latex.preamble'] = [ r'\usepackage{siunitx}' ]
mpl.rcParams['text.usetex'] = True

def decay( ts, init, tau ):
    res = np.zeros_like( ts )
    res[0] = init 
    for i, t in enumerate( ts[1:] ):
        dt = ts[i+1] - ts[i]
        rands = np.random.random( int(res[i]) )
        ndecay = len( rands[ rands < (dt / tau) ] )
        res[i+1] = res[i] - ndecay 
    return res

def main( ):
    tau1, tau2 = 1, 100
    ts = np.arange( 0, 50, 0.1 )
    y1 = decay( ts, 40, tau1 )
    y2 = decay( ts, 40, tau2 )
    plt.subplot( 211 )
    plt.plot( ts, y1, label = 'fast' )
    plt.plot( ts, y2, label = 'slow' )
    plt.plot( ts, (y1 +  y2)/2.0, color='blue', label = 'slow + fast' )
    plt.legend( )
    plt.subplot( 212 )
    plt.plot( ts, y1 + y2, color='blue', label = 'slow + fast' )
    plt.legend( )
    plt.xlabel( 'time' )
    plt.savefig( 'test_two_tau.png' )


if __name__ == '__main__':
    main()
