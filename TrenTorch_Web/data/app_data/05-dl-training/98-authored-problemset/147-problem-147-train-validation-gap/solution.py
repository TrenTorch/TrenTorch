import numpy as np

def solve(train_loss, val_loss):
    """Implement train/validation gap according to the contract."""
    return float(val_loss - train_loss)
