def missing_number(nums):
    n = len(nums)
    return n * (n + 1) // 2 - sum(nums)
