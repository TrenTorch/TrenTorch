def rotate_left(nums, k):
    if not nums:
        return []
    k %= len(nums)
    return nums[k:] + nums[:k]
