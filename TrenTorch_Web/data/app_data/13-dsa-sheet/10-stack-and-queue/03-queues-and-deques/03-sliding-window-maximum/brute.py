def sliding_window_max(nums, k):
    return [max(nums[i : i + k]) for i in range(len(nums) - k + 1)]
