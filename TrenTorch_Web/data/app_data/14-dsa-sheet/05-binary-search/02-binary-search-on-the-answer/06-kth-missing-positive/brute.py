def kth_missing_positive(nums, k):
    seen = set(nums)
    n = 0
    while k:
        n += 1
        if n not in seen:
            k -= 1
    return n
