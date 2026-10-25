def count_reverse_pairs(nums):
    n = len(nums)
    return sum(1 for i in range(n) for j in range(i + 1, n) if nums[i] > 2 * nums[j])
