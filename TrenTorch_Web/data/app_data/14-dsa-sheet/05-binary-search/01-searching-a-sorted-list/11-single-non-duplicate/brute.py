def single_non_duplicate(nums):
    result = 0
    for x in nums:
        result ^= x
    return result
