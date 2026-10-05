import numpy as np

def solve(values, categories):
    categories = list(categories)
    positions = {category: i for i, category in enumerate(categories)}
    out = np.zeros((len(values), len(categories)), dtype=int)
    for row, value in enumerate(values):
        out[row, positions[value]] = 1
    return out
