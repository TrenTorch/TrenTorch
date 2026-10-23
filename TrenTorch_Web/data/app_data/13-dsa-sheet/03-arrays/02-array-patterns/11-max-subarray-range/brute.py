def max_subarray_range(nums):
    best = None
    for i in range(len(nums)):
        total = 0
        for j in range(i, len(nums)):
            total += nums[j]
            key = (total, -i, -(j - i))
            if best is None or key > best[0]:
                best = (key, [total, i, j])
    return best[1]
