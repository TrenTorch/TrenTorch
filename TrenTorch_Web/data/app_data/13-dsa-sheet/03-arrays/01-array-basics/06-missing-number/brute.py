def missing_number(nums):
    present = set(nums)
    return next(v for v in range(len(nums) + 1) if v not in present)
