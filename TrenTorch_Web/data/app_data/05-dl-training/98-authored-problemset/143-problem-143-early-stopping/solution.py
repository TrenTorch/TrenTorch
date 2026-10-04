import numpy as np

def solve(losses, patience):
    """Early stopping resets its bad-epoch count whenever validation loss strictly improves and stops after patience consecutive non-improving epochs."""
    best=float("inf"); bad=0
    for loss in losses:
        if loss<best: best=loss; bad=0
        else:
            bad+=1
            if bad>=patience: return True
    return False
