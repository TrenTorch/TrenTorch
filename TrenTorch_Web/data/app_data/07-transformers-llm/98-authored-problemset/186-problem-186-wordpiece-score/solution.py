import numpy as np

def solve(pair_count, left_count, right_count):
    """Implement wordpiece score according to the contract."""
    return pair_count / (left_count * right_count)
