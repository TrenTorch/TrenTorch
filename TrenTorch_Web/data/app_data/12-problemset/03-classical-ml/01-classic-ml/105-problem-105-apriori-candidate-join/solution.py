import numpy as np

def solve(prev):
    """Apriori joins lexicographically ordered (k-1)-itemsets with matching first k-2 items, appending the final item to form k-item candidates."""
    prev = sorted(map(tuple, prev))
    out = set()
    for a in range(len(prev)):
        for b in range(a + 1, len(prev)):
            if prev[a][:-1] == prev[b][:-1]:
                out.add(prev[a] + (prev[b][-1],))
    return sorted(out)
