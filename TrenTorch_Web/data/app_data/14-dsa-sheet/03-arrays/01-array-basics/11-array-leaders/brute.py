def array_leaders(nums):
    return [x for i, x in enumerate(nums) if all(x > y for y in nums[i + 1 :])]
