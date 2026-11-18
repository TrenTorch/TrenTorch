def kth_largest(nums, k):
    return sorted(nums, reverse=True)[k - 1]
