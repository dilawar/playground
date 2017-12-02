#!/usr/bin/env python

"""peri_demo.py: 

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
import peri
import peri.util
from peri.viz.interaction import OrthoViewer
from peri.viz.interaction import OrthoPrefeature 
import peri.comp 

def main( ):
    tiff = peri.util.RawImage( './small_confocal_image.tif' )
    objs = peri.comp.objs.Slab( zpos = 6 )
    ppos = np.load( './particle-positions.npy' )
    print( ppos )
    prad = 5.0
    particles = peri.comp.objs.PlatonicSpheresCollection( ppos, prad )
    OrthoPrefeature( tiff.get_image( ), ppos, viewrad = 3 )
    plt.savefig( 'tmp.png' )

if __name__ == '__main__':
    main()
