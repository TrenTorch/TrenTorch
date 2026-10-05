import numpy as np

def solve(y, pred):
    y = np.asarray(y)
    pred = np.asarray(pred)
    return np.array([[np.sum((y == 0) & (pred == 0)), np.sum((y == 0) & (pred == 1))], [np.sum((y == 1) & (pred == 0)), np.sum((y == 1) & (pred == 1))]])
