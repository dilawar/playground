import numpy as np

class TimeSeries():

    def __init__(self):
        self.data = None
        self.spikes = []

    def load(self, data):
        self.data = np.array(data)

    def __repr__(self):
        return str(self.data)

    def findElem(self, val):
        return self.data[self.data == val]

    def loadCSV(self, filename):
        return np.loadtxt(filename)

    def plot(self, outfile=None):
        import matplotlib.pyplot as plt
        plt.plot(self.data)
        if outfile is None:
            plt.show()

