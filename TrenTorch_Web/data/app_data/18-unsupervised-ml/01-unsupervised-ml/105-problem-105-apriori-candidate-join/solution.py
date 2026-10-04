import numpy as np

def solve(prev):
    """Implement apriori candidate join according to the contract."""
    prev = sorted(map(tuple, prev))
    out = set()
    for a in range(len(prev)):
        for b in range(a + 1, len(prev)):
            if prev[a][:-1] == prev[b][:-1]:
                out.add(prev[a] + (prev[b][-1],))
    return sorted(out)
