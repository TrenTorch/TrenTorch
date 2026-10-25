def max_sum_k(nums, k):
    return max(sum(nums[i : i + k]) for i in range(len(nums) - k + 1))
