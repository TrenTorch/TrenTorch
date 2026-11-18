def min_subset_difference(nums):
    total = sum(nums)
    best = total
    for mask in range(1 << len(nums)):
        s = sum(nums[i] for i in range(len(nums)) if mask >> i & 1)
        best = min(best, abs(total - 2 * s))
    return best
