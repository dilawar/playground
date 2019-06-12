#!/usr/bin/env python

"""color_bees.py: 

"""
    
__author__           = "Dilawar Singh"
__copyright__        = "Copyright 2017-, Dilawar Singh"
__version__          = "1.0.0"
__maintainer__       = "Dilawar Singh"
__email__            = "dilawars@ncbs.res.in"
__status__           = "Development"

import sys
import os
import itertools

colors_ = "YWPOGB"
pos_ = "123"

def main( args ):
    nLoc = len( args.locations )
    combs = itertools.product( args.colors, repeat = nLoc )
    print( "BeesIndex,Colors" )
    for i, c in enumerate( combs ):
        print( "%d,%s" % (i, ''.join(c)) )

if __name__ == '__main__':
    import argparse
    # Argument parser.
    description = '''Colorsize bees'''
    parser = argparse.ArgumentParser(description=description)
    parser.add_argument('--colors', '-c'
        , required = False
        , default = "YWPOGB"
        , help = 'Colors I have.'
        )
    parser.add_argument('--locations', '-l'
        , required = False
        , default = "123"
        , help = 'Locations on bees'
        )
    class Args: pass 
    args = Args()
    parser.parse_args(namespace=args)
    main( args )
