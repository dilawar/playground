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
    x = (x - offset)/1e-3
    return np.exp(-(x/a)**2) / abs(a) / math.pi**0.5

def compute_approx(ts, spikes):
    y = np.zeros_like(ts)
    for spk in spikes:
        y += dirac_delta(ts, 1, spk)
    return y

def main():
    T = np.linspace(0, 20e-3, 100)
    spikes = [1e-3, 5e-3, 12e-3]
    v = compute_approx(T, spikes)
    ax1 = plt.subplot(211)

    ax2 = plt.subplot(212)
    ax2.plot(T, v)
    plt.show()

if __name__ == '__main__':
    main()
