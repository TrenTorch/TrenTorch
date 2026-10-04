import numpy as np

def solve(logits):
    """Implement greedy decoding according to the contract."""
    return int(np.argmax(logits))
