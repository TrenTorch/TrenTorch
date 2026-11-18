from itertools import combinations


def palindrome_partitions(s):
    n = len(s)
    out = []
    for r in range(n):
        for cuts in combinations(range(1, n), r):
            bounds = [0, *cuts, n]
            pieces = [s[bounds[i] : bounds[i + 1]] for i in range(len(bounds) - 1)]
            if all(p == p[::-1] for p in pieces):
                out.append(pieces)
    return sorted(out) if n else [[]]
