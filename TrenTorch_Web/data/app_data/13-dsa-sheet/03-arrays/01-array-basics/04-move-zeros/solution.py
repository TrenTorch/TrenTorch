def move_zeros(nums):
    return [x for x in nums if x != 0] + [0] * nums.count(0)
