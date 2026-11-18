def max_xor_pair(nums):
    return max(a ^ b for a in nums for b in nums)
