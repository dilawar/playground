import pylab
import numpy as np

a = np.array([0, 0, 0, 1, 1, 0, 0, 0])
b = np.array([0, 0, 0, 0, 0, 1, 1, 0])

c = np.correlate(a, b, 'same')
print a
print b
print c
