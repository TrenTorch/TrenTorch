def find_duplicate(nums):
    return next(x for i, x in enumerate(nums) if x in nums[:i])
