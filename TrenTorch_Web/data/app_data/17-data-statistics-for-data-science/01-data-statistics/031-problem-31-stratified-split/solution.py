import numpy as np

def solve(y, test_size=0.2, seed=0):
    """Implement stratified split according to the contract."""
    rng = np.random.default_rng(seed)
    train = []
    test = []
    for c in np.unique(y):
        idx = np.where(np.asarray(y) == c)[0]
        rng.shuffle(idx)
        k = int(len(idx) * test_size)
        test.extend(idx[:k])
        train.extend(idx[k:])
    return (np.array(sorted(train)), np.array(sorted(test)))
