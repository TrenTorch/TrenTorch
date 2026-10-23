def max_consecutive_ones(nums):
    best = current = 0
    for x in nums:
        if x == 1:
            current += 1
            best = max(best, current)
        else:
            current = 0
    return best
