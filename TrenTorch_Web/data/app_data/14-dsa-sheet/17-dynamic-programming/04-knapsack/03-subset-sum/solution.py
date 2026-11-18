def subset_sum(nums, target):
    mask = (1 << (target + 1)) - 1
    bits = 1
    for x in nums:
        bits |= (bits << x) & mask
    return bits >> target & 1 == 1
