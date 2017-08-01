"""test_dict_sorting.py: 

This script is from
https://writeonly.wordpress.com/2008/08/30/sorting-dictionaries-by-value-in-python-improved/#comment-12912

I've just plotted the results; thats all.

"""
    
__author__           = "Dilawar Singh"
__copyright__        = "Copyright 2017-, Dilawar Singh"
__version__          = "1.0.0"
__maintainer__       = "Dilawar Singh"
__email__            = "dilawars@ncbs.res.in"
__status__           = "Development"

import sys
import os


def sbv0(adict,reverse=False):
    ''' proposed at Digital Sanitation Engineering
    http://blog.modp.com/2007/11/sorting-python-dict-by-value.html '''
    return sorted(adict.items(), key=lambda x: (x[1],x[0]), reverse=reverse)
 
def sbv1(d,reverse=False):
    '''  explicit list expansion '''
    L = [(k,v) for (k,v) in d.items()]
    return sorted(L, key=lambda x: x[1] , reverse=reverse)
 
def sbv2(d,reverse=False):
    '''  generator '''
    L = ((k,v) for (k,v) in d.items())
    return sorted(L, key=lambda x: x[1] , reverse=reverse)
 
def sbv3(d,reverse=False):
    ''' using a lambda to get the key, rather than "double-assignment" '''
 
    return sorted(d.items(), key=lambda x: x[1] , reverse=reverse)
 
def sbv4(d,reverse=False):
    ''' using a formal function to get the sorting key, rather than a lambda'''
    def sk(x):  return x[1]
    return sorted(d.items(), key=sk , reverse=reverse)
 
def sk(x):  return x[1]
 
def sbv5(d,reverse=False):
    ''' using a formal function, defined in outer scope
    to get the sorting key, rather than a lambda
    '''
    return sorted(d.items(), key=sk , reverse=reverse)
 
from operator import itemgetter
def sbv6(d,reverse=False):
    ''' proposed in PEP 265, using  the itemgetter '''
    return sorted(d.items(), key=itemgetter(1), reverse=True)
 
d_ = dict(zip(range(100),range(100)))

def main( ):
    import timeit
    for mI in range( 7 ):
        methodName = "sbv%d" % mI
        cmd = "for ii in range(10000):  %s(d_, reverse=True)" % methodName 
        N = 20
        t = timeit.timeit( cmd, number=N
                , setup="from __main__ import %s, d_" % methodName 
                )
        print( "%s took %.4f seconds on average (N=%d)" % (methodName, t / N, N ) )

if __name__ == '__main__':
    main()
