"""car_behind_3doors.py: 

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


def play(switch):
    doors = ['E', 'E', 'C']
    random.shuffle(doors)
    #  print( doors )
    pickI = random.choice([0,1,2])
    empty = doors.index('E')
    while empty == pickI:
        empty = pickI + 1 + doors[pickI+1:].index('E')

    if switch:
        otherDoors = list(set([0,1,2])-set([pickI, empty]))
        pickI = random.choice(otherDoors)

    #  print( f'I pick {pickI} and gamer empty door is {empty}' )
    if doors[pickI] == 'C':
        return True
    return False


def play_game(N, switch=False):
    print(N, switch)
    nWin = 0
    for i in range(N):
        win = play(switch)
        if win:
            nWin += 1
    return nWin/N

def main():
    N = 30000
    p = play_game(N, False)
    print(p)
    p = play_game(N, True)
    print(p)

if __name__ == '__main__':
    main()

