def min_subset_difference(nums):
    total = sum(nums)
    bits = 1
    for x in nums:
        bits |= bits << x
    for s in range(total // 2, -1, -1):
        if bits >> s & 1:
            return total - 2 * s
    return total
