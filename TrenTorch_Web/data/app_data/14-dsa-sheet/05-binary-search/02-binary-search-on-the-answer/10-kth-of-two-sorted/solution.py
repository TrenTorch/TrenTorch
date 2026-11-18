def kth_of_two_sorted(a, b, k):
    if len(a) > len(b):
        a, b = b, a
    m, n = len(a), len(b)
    lo, hi = max(0, k - n), min(k, m)
    while lo <= hi:
        i = (lo + hi) // 2
        j = k - i
        a_left = a[i - 1] if i > 0 else float("-inf")
        a_right = a[i] if i < m else float("inf")
        b_left = b[j - 1] if j > 0 else float("-inf")
        b_right = b[j] if j < n else float("inf")
        if a_left <= b_right and b_left <= a_right:
            return max(a_left, b_left)
        if a_left > b_right:
            hi = i - 1
        else:
            lo = i + 1
