"""two_dist_bis_normal.py: 

Normal and Bimoal distribution.

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

volumes = np.random.gamma( 2., 0.1, 1000)

channels = np.hstack( 
        ( np.random.normal( .70, .1, 1000 ), np.random.normal( .10, .1, 1000 ) )
        )

plt.subplot( 211 )
plt.hist( volumes, bins = 100 )

plt.subplot( 212 )
plt.hist( channels, bins = 100 )

plt.show( )

