import sys
import os
import scipy.optimize as sco
import numpy as np
import matplotlib.pyplot as plt
from scipy.special import gamma

def func( x, A0, tau ):
    f1 = A0 * np.exp( -x/tau ) 
    return f1 + gamma_dist(x) 

def gamma_dist( x, P = 99.13, k = 7.89, theta = 0.109 ):
    f2 = P * x**(k-1) * np.exp(-x/theta) / theta**k / gamma(k)
    return f2

def main( ):
    data = np.loadtxt( './data_insertion_freq.csv', delimiter = ','
            , skiprows = 1 )
    print( data.shape )
    x, y = data[:,0] / 10000, data[:,1]
    plt.plot( x, y )

    # fit
    p0 = [ 300, 10, 150, 4, 0.25  ]
    #  popt, pcov = sco.curve_fit( func, x, y, p0 = p0 )
    popt, pcov = sco.curve_fit( func, x, y )
    print( "Params : %s" % popt )
    plt.plot( x, func(x, *popt ), label = 'fit' )
    plt.legend( )

    plt.savefig( '%s.png' % sys.argv[0] )

if __name__ == '__main__':
    main()
