def smallest_divisor(nums, threshold):
    for d in range(1, max(nums) + 1):
        if sum(-(-x // d) for x in nums) <= threshold:
            return d
