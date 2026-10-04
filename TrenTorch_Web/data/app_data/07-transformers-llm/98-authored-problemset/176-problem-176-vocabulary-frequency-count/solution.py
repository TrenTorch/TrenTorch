import numpy as np
from collections import Counter

def solve(tokens, k):
    """Implement vocabulary frequency count according to the contract."""
    from collections import Counter
    return Counter(tokens).most_common(k)
