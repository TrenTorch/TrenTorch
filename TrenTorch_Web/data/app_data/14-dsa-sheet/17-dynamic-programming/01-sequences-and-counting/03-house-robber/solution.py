def rob(nums):
    skip = take = 0
    for x in nums:
        skip, take = max(skip, take), skip + x
    return max(skip, take)
