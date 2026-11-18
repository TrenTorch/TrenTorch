def nth_root(n, m):
    lo, hi = 1, 1 << (n.bit_length() // m + 1)
    while lo <= hi:
        mid = (lo + hi) // 2
        power = mid**m
        if power == n:
            return mid
        if power < n:
            lo = mid + 1
        else:
            hi = mid - 1
    return -1
