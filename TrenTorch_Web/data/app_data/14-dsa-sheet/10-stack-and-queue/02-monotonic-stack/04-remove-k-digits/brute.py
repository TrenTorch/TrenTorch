from itertools import combinations


def remove_k_digits(num, k):
    keep = len(num) - k
    if keep <= 0:
        return "0"
    best = min(int("".join(c)) for c in combinations(num, keep))
    return str(best)
