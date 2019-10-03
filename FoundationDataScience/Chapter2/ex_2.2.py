__author__           = "Dilawar Singh"
__copyright__        = "Copyright 2019-, Dilawar Singh"
__maintainer__       = "Dilawar Singh"
__email__            = "dilawars@ncbs.res.in"

import sys
import os
import math
import matplotlib.pyplot as plt
import numpy as np
import itertools

pts = np.random.random(size=(30,1000)) - 0.5

for p1, p2 in itertools.product(pts, repeat=2):
    d = sum(p1**2 - p2**2)**0.5
    cosine = np.dot(p1, p2)/np.linalg.norm(p1, 2)/np.linalg.norm(p2, 2)
    if d != 0:
        print(d, 180*math.acos(cosine)/math.pi)
    else:
        print(0, 90)


