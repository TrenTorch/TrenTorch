def number_of_subarrays(nums, k):
    return sum(
        1
        for i in range(len(nums))
        for j in range(i, len(nums))
        if sum(x % 2 for x in nums[i : j + 1]) == k
    )
