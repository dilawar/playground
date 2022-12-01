import numpy as np
import pandas as pd

data = pd.read_csv('./input')
y = data.diff()
y = y[y > 0].dropna()
print(len(y))
