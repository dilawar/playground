"""so_group_tuple.py: 

"""

import sys
import collections
import itertools
import os
import random
import operator
import time


def group_coldspeed( a ):
    o = collections.OrderedDict( )
    for x in a:
        o.setdefault( x[0], [ ]).append( x[1] )
    return list( o.items( ) )

def group_pm2ring( a ):
    b = [(k, list(list(zip(*g))[1])) for 
            k, g in itertools.groupby(a, operator.itemgetter(0))]
    return b

def main( ):
    N = 100000
    a = [ (random.randint(1, 20), random.randint(1, 10000)) for i in range(N) ]
    a = sorted( a )
    t = time.time( )
    r1 = group_coldspeed( a )
    print( 'Time taken %f' % (time.time( ) - t ) )
    t = time.time( )
    r2 = group_pm2ring( a )
    print( 'Time taken %f' % (time.time( ) - t ) )
    assert r1 == r2


if __name__ == '__main__':
    main()

