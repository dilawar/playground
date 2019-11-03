import numpy as np
import random
import sys
from timeseries import TimeSeries

print('Arguments are ', sys.argv)

t = TimeSeries()
t.load([1,2,3,4])
t.plot()

