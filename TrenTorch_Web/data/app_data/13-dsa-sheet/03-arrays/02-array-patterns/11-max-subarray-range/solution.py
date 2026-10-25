def max_subarray_range(nums):
    best = [nums[0], 0, 0]
    current = nums[0]
    begin = 0
    for i in range(1, len(nums)):
        if current < 0:
            current = nums[i]
            begin = i
        else:
            current += nums[i]
        if current > best[0]:
            best = [current, begin, i]
    return best
