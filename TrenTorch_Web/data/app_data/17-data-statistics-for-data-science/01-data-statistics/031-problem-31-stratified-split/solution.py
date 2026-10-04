import numpy as np

def solve(y, test_size=0.2, seed=0):
    rng = np.random.default_rng(seed)
    train, test = [], []
    y = np.asarray(y)
    for label in np.unique(y):
        indices = np.where(y == label)[0]
        rng.shuffle(indices)
        count = int(len(indices) * test_size)
        test.extend(indices[:count])
        train.extend(indices[count:])
    return np.asarray(sorted(train), dtype=int), np.asarray(sorted(test), dtype=int)
