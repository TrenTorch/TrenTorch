from itertools import combinations


def min_cut_palindromes(s):
    n = len(s)
    if n == 0:
        return 0
    for k in range(n):
        for cut in combinations(range(1, n), k):
            bounds = [0, *cut, n]
            pieces = [s[bounds[i] : bounds[i + 1]] for i in range(len(bounds) - 1)]
            if all(p == p[::-1] for p in pieces):
                return k
    return n - 1
