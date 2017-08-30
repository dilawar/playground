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

# For N = 5000, k = 500, it takes ever to solve.
N, k = 1000, 200
t = np.arange( 0, 1/8.0, 1.0 / (N * 8.0) )
atone = np.sin( 1394 * math.pi * t ) + np.sin( 3266 * math.pi * t )
np.savetxt( '_tone.dat', np.vstack((t, atone)).T )

ax1.plot( t, atone )
ax1.set_title( 'Signal x. N = %d' % N )

atoneDct = scipy.fftpack.dct( atone, norm = 'ortho' )
np.savetxt( '_tone_dct.dat', atoneDct )
ax2.plot( atoneDct )
ax2.set_title( '$\phi$ = DCT(x)' )
#  ax2.set_xlim( [0, 600 ])


# random sampling
A = np.random.randn( k, N )
np.savetxt( '_measurement_matrix_dct.dat', A )
sampleI = np.random.choice( range( len( atone ) ), k )
fig = ax3.imshow( A, aspect = 'auto' )
ax3.set_title( 'Mask A' )
plt.colorbar( fig, ax = ax3 )

# Sample using A
b = np.dot( A, atoneDct )
np.savetxt( '_measurements_dct.dat', b )


ax4.plot( b )
ax4.set_title(  'b =A $\phi$' )
ax4.legend(loc='best', framealpha=0.4)


print( 'Solving using CS' )
# compressed sensing solution.
print( atoneDct.shape, A.shape, b.shape )
x0 =  np.dot( A.T, b )
print( 'Computed x0' )
bcs = l1eq_pd( x0, A, [ ], b )
np.savetxt( '_result_dct.dat', bcs )
print( 'Error', np.linalg.norm( x0 - bcs ) )

ax5.plot( bcs )
#  ax4.set_xlim( [0, 600 ] )
ax5.set_title( "$\phi = \min_\phi L_1(\phi) \;, A \phi=b$ " )

# reconstruction.
res = scipy.fftpack.idct( bcs, norm = 'ortho' )
np.savetxt( '_result_tone.dat', np.vstack( (t, res) ).T )
ax6.plot( t, res )

plt.tight_layout( pad = 2 )
plt.savefig( 'magic_reconstruction.png' )
