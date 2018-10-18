"""ode_system.py: 

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
import sympy as _s
from sympy.abc import *

def system( ):
    A, B, C = _s.symbols( "A B C", cls=_s.Function)
    t = _s.abc.t
    eq1 = _s.Eq(A(t).diff(t), 1)
    eq2 = _s.Eq(B(t).diff(t), 2)
    return (eq1, eq2), (A,B)

def main():
    _s.init_printing()
    sys, vs = system()
    r = _s.dsolve(sys )
    print( r )


if __name__ == '__main__':
    main()
