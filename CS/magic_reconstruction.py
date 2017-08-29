"""magic_reconstruction.py: 

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

N, k = 5000, 200
t = np.arange( 0, 1/8.0, 1.0 / 40000  )
atone = np.sin( 1394 * math.pi * t ) + np.sin( 3266 * math.pi * t )

ax1.plot( t, atone )
ax1.set_title( 'Signal (Tone A)' )

atoneDct = scipy.fftpack.dct( atone, norm = 'ortho' )
ax2.plot( atoneDct )
ax2.set_title( 'DCT' )
ax2.set_xlim( [0, 600 ])


# random sampling
sampleI = np.random.choice( range( len( atone ) ), k )
samples = atone[ sampleI ]
dctSamples = atoneDct[ sampleI ]
ax3.plot( samples )
ax3.set_title( 'b, %s samples' % k )

D = scipy.fftpack.dct( np.eye(N, N) )
A = D[ sampleI, : ]
fig = ax4.imshow( A, aspect = 'auto' )
ax4.set_title( 'A, underdetermined in DCT domain' )
plt.colorbar( fig, ax = ax4 )

# l2 solution.
b = np.matrix( samples )
print( 'Solving Ax = b using L2 norm. Moore-Penrose inverse' )
b1 = scipy.linalg.pinv( A ) * b.T


ax5.plot( b1 )
ax5.set_xlim( [0, 600 ] )
ax5.set_title( 'x = $A^+$ * b, $L_2$ norm' )

# compressed sensing solution.
print( atoneDct.shape, A.shape, b.shape )
x0 =  atoneDct
y = np.matrix( b.T )
#  print( "x0: %s, y: %s, A:%s" % (x0.shape, y.shape, A.shape) )
bcs = l1eq_pd( x0, A, np.array([]), y )
print( 'Error', np.linalg.norm( bcs - x0 ) )
ax6.plot( bcs )
ax6.set_xlim( [0, 600 ] )
ax6.set_title( 'x = minimize l1(x); $Ax=b$ ' )

plt.tight_layout( pad = 2 )
plt.savefig( 'magic_reconstruction.png' )
