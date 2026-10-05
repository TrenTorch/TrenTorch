import numpy as np

def solve(results):
    """Grid search selects the result record with the smallest validation loss; ties use the string form of params for deterministic ordering."""
    return min(results,key=lambda r:(r["val_loss"],str(r["params"]))) if results else None
