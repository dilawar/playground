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
    for i in range( 1, 7 ):
        N = 10 ** i
        a = [ (random.randint(1, 20), random.randint(1, 10000)) for i in range(N) ]
        a = sorted( a )
        times = [ ]
        for method in [ group_coldspeed , group_pm2ring ]:
            t = time.time( )
            r1 = method( a )
            times.append( '%.4f' % (time.time( ) - t ))
        print( str(N) + ' ' +  ' '.join(times) )


if __name__ == '__main__':
    main()

