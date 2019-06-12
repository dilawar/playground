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
import random


s1, s2 = [ ], [ ]

N = 0
while True:
    N += 1
    doors =  [ 'c', 'g', 'g' ]
    doorIndex = [0,1,2]
    random.shuffle( doors )
    myChoice = random.choice(doorIndex )
    msg = ''.join(doors)

    msg += ' | Pick %d ' % (myChoice+1)
    goatDoor = random.choice( doorIndex )
    while goatDoor == myChoice or doors[ goatDoor ] != 'g':
        goatDoor = random.choice( doorIndex )

    doorsLeft = set(doorIndex) - set( [myChoice, goatDoor])
    doorLeft = list(doorsLeft)[0]
    msg += '| %d has goat ' % (goatDoor+1)
    s1.append( 'W' if doors[ myChoice ] == 'c' else 'L' )
    s2.append( 'W' if doors[ doorLeft ] == 'c' else 'L' )
    msg += '| Dont change: %s | Change: %s ' % ( s1[-1], s2[-1] )
    print( msg )
    e = raw_input( 'Press q to exit. Any other key to continue: ' )
    if e == 'q':
        break

print( '\n===============' )
print( 'Total games = %d' % N )
print( 'DONT CHANGE Wins %d' % s1.count( 'W' ) )
print( 'ALWAYS CHANGE Wins %d' % s2.count( 'W' ) )


