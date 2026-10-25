def subarrays_k_distinct(nums, k):
    return sum(
        1
        for i in range(len(nums))
        for j in range(i, len(nums))
        if len(set(nums[i : j + 1])) == k
    )
