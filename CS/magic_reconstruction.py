"""magic_reconstruction.py: 

    still not working.
"""
    
__author__           = "Dilawar Singh"
__copyright__        = "Copyright 2017-, Dilawar Singh"
__version__          = "1.0.0"
__maintainer__       = "Dilawar Singh"
__email__            = "dilawars@ncbs.res.in"
__status__           = "Development"

import sys
import os
import numpy as np
import math
import scipy.fftpack
import scipy.linalg
import scipy.optimize

import matplotlib as mpl
import matplotlib.pyplot as plt
from pyCSalgos.BP.l1eq_pd import l1eq_pd


try:
    mpl.style.use( 'classic' )
except Exception as e:
    pass
mpl.rcParams['axes.linewidth'] = 0.1
plt.rc('text', usetex=True)
plt.rc('font', family='serif')


plt.figure( figsize = (12, 8 ) )
gridSize = (3, 2)
ax1 = plt.subplot2grid( gridSize, (0,0), colspan = 1 )
ax2 = plt.subplot2grid( gridSize, (0,1), colspan = 1 )
ax3 = plt.subplot2grid( gridSize, (1,0), colspan = 1 )
ax4 = plt.subplot2grid( gridSize, (1,1), colspan = 1 )
ax5 = plt.subplot2grid( gridSize, (2,0), colspan = 1 )
ax6 = plt.subplot2grid( gridSize, (2,1), colspan = 1 )

N, k = 500, 50
t = np.arange( 0, 1/8.0, 1.0 / (N * 8.0) )
atone = np.sin( 1394 * math.pi * t ) + np.sin( 3266 * math.pi * t )

ax1.plot( t, atone )
ax1.set_title( 'Signal (Tone A)' )

atoneDct = scipy.fftpack.dct( atone, norm = 'ortho' )
ax2.plot( atoneDct )
ax2.set_title( 'DCT' )
ax2.set_xlim( [0, 600 ])


# random sampling
sampleI = np.random.choice( range( len( atone ) ), k )
b = atone[ sampleI ]
dctSamples = atoneDct[ sampleI ]

A = np.random.randn( k, N )
print( A.shape )

# l2 solution.
print( 'Solving Ax = b using L2 norm. Moore-Penrose inverse' )
b1 = np.dot( scipy.linalg.pinv( A ), b )

print( 'Solving using CS' )
ax3.plot( b1 )
ax3.set_xlim( [0, 600 ] )
ax3.set_title( '$\phi$ = $A^+$ * b, $L_2$ norm' )

# compressed sensing solution.
print( atoneDct.shape, A.shape, b.shape )
x0 =  np.dot( A.T, b )
print( 'Computed x0' )
bcs = l1eq_pd( x0, A, [ ], b )
print( 'Error', np.linalg.norm( x0 - bcs ) )
ax4.plot( bcs )
ax4.set_xlim( [0, 600 ] )
ax4.set_title( '$\phi$ = minimize l1(x); $Ax=b$ ' )

# reconstruction.
ax5.plot( t, scipy.fftpack.idct( b1, norm = 'ortho' ) )
ax6.plot( t, scipy.fftpack.idct( bcs, norm = 'ortho' ) )

plt.tight_layout( pad = 2 )
plt.savefig( 'magic_reconstruction.png' )
