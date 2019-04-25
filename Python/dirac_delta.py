"""dirac_delta.py: 

"""
    
__author__           = "Dilawar Singh"
__copyright__        = "Copyright 2017-, Dilawar Singh"
__version__          = "1.0.0"
__maintainer__       = "Dilawar Singh"
__email__            = "dilawars@ncbs.res.in"
__status__           = "Development"

import sys
import os
import math
import matplotlib.pyplot as plt
import numpy as np

def dirac_delta(x, a, offset=0):
    x = x - offset
    return np.exp(-(x/a)**2) / abs(a) / math.pi**0.5

def main():
    x = np.linspace(-10, 10, 1000)
    y1 = dirac_delta(x, 1, 1)
    y2 = dirac_delta(x, 2, 0)
    plt.plot(x, y1)
    plt.plot(x, y2)
    plt.show()

if __name__ == '__main__':
    main()
