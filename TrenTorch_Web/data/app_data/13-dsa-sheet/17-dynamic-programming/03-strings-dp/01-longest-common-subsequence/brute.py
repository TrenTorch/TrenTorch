from itertools import combinations


def lcs_length(a, b):
    for size in range(len(a), 0, -1):
        subs = {"".join(c) for c in combinations(a, size)}
        for sub in subs:
            it = iter(b)
            if all(ch in it for ch in sub):
                return size
    return 0
