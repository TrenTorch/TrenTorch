import numpy as np

def solve(forward, backward):
    """Implement bidirectional rnn merge according to the contract."""
    return np.concatenate([forward, backward], axis=-1)
