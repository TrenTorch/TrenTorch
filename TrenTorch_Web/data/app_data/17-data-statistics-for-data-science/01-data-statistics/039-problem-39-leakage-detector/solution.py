import numpy as np

def solve(columns):
    """Implement leakage detector according to the contract."""
    forbidden = ('target', 'label', 'future', 'outcome', 'post_')
    return [c for c in columns if any((k in c.lower() for k in forbidden))]
