import numpy as np

def solve(predictions, y):
    predictions = np.asarray(predictions, dtype=float)
    y = np.asarray(y, dtype=float)
    mean_prediction = predictions.mean(axis=0)
    squared_bias = np.mean((mean_prediction - y) ** 2)
    variance = np.mean(np.var(predictions, axis=0))
    return float(squared_bias), float(variance)
