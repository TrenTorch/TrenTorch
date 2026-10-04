import numpy as np

def solve(logits):
        return int(np.argmax(logits))
