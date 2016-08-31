"""test_stochastic.py: 

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
import matplotlib
import matplotlib.pyplot as plt
import numpy as np

import moose
import moose.utils as mu

try:
    matplotlib.style.use( 'poster' )
except Exception as e:
    pass

cyl = moose.CylMesh( '/cyl' )
cyl.volume = 1e-20

species = {}
tables = {}
for sp in [ 'a', 'b', 'c', 'd' ]:
    species[sp] = moose.Pool( '%s/%s' % (cyl.path, sp) )
    tab = moose.Table2( '%s/tab' % species[sp].path )
    moose.connect( tab, 'requestOut', species[sp], 'getN' )
    tables[sp] = tab
    
species['a'].nInit = 20.0
species['b'].nInit = 5.0
species['c'].nInit = 0.0
species['d'].nInit = 1.0

r1 = moose.Reac( '%s/reac' % cyl.path )

f1 = moose.Function( '/cyl/f1' )
f1.expr = '10.0+sin(100*t)'
moose.connect( f1, 'valueOut', r1, 'setNumKf' )
r1.numKb = 10.0

moose.connect( r1, 'sub', species['a'], 'reac')
# moose.connect( r1, 'sub', species['a'], 'reac')
# moose.connect( r1, 'sub', species['b'], 'reac')
moose.connect( r1, 'sub', species['b'], 'reac')
moose.connect( r1, 'prd', species['c'], 'reac')
# moose.connect( r1, 'prd', species['d'], 'reac')
moose.connect( r1, 'prd', species['d'], 'reac')

stoich = moose.Stoich( '%s/stoich' % cyl.path )
gsolve = moose.Gsolve( '%s/gsolve' % cyl.path )
stoich.ksolve = gsolve
stoich.compartment = cyl
stoich.path = '%s/##' % cyl.path

moose.reinit()
moose.start( 100000, 1 )
# mu.plotRecords( tables, subplots = True, outfile = "result.png" )
plots = []
for i, tab in enumerate(tables):
    plots.append( tables[tab].vector )
    plt.subplot( len(tables) + 1, 1, i + 1)
    plt.plot( plots[-1], label = tab )
    plt.legend(loc='best', framealpha=0.4)

plt.subplot( len(plots) + 1, 1, len(plots) + 1 )
plt.plot( np.sum(plots, axis=0), label = 'sum of all species' )
plt.legend(loc='best', framealpha=0.4)
plt.tight_layout( )
plt.savefig( '%s.png' % sys.argv[0] )
