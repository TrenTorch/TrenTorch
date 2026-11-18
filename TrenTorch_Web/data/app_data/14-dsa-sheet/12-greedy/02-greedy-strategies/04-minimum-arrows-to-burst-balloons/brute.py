from itertools import combinations


def min_arrows(points):
    if not points:
        return 0
    spots = sorted({end for _, end in points})
    for k in range(1, len(spots) + 1):
        for chosen in combinations(spots, k):
            if all(any(s <= x <= e for x in chosen) for s, e in points):
                return k
