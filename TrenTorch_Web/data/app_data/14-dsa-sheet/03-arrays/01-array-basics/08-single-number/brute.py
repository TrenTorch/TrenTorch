def single_number(nums):
    counts = {}
    for x in nums:
        counts[x] = counts.get(x, 0) + 1
    return next(x for x, c in counts.items() if c == 1)
