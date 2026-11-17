def sorted_squares(nums):
    out = [0] * len(nums)
    left, right = 0, len(nums) - 1
    for i in range(len(nums) - 1, -1, -1):
        if abs(nums[left]) > abs(nums[right]):
            out[i] = nums[left] ** 2
            left += 1
        else:
            out[i] = nums[right] ** 2
            right -= 1
    return out
