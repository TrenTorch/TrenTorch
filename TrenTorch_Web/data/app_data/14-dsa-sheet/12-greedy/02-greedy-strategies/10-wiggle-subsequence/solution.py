def wiggle_length(nums):
    if not nums:
        return 0
    length = 1
    direction = 0
    for i in range(1, len(nums)):
        diff = nums[i] - nums[i - 1]
        if diff > 0 and direction <= 0:
            length += 1
            direction = 1
        elif diff < 0 and direction >= 0:
            length += 1
            direction = -1
    return length
