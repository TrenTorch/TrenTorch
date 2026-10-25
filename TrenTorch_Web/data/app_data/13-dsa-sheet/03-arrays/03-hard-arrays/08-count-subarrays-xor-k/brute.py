def count_subarrays_xor_k(nums, k):
    count = 0
    for i in range(len(nums)):
        value = 0
        for j in range(i, len(nums)):
            value ^= nums[j]
            if value == k:
                count += 1
    return count
