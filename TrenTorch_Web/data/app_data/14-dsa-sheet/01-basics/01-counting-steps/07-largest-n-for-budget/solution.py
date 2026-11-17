def _cost(growth, n):
    if growth == "n":
        return n
    if growth == "n log n":
        return n * (n.bit_length() - 1)
    if growth == "n^2":
        return n * n
    return n * n * n


def largest_n(growth, budget):
    if growth == "2^n":
        return max(budget.bit_length() - 1, 0) if budget >= 2 else 0
    if _cost(growth, 1) > budget:
        return 0
    lo, hi = 1, budget + 1
    while lo < hi:
        mid = (lo + hi + 1) // 2
        if _cost(growth, mid) <= budget:
            lo = mid
        else:
            hi = mid - 1
    return lo
