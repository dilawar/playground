"""monty_hall.py: 

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
import random

def main( ):
    doors = [ 'Car', 'Goat', 'Nothing' ]
    for i in range( 2000 ):
        random.shuffle( doors )
        print( doors )



if __name__ == '__main__':
    main()
