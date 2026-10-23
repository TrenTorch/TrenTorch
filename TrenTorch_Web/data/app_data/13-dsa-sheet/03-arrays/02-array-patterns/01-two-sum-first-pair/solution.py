def two_sum_first_pair(nums, target):
    first = {}
    best = None
    for j, x in enumerate(nums):
        i = first.get(target - x)
        if i is not None and (best is None or (i, j) < best):
            best = (i, j)
        if x not in first:
            first[x] = j
    return [-1, -1] if best is None else list(best)
