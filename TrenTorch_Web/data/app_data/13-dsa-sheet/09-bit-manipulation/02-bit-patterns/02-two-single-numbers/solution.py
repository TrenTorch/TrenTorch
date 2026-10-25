def two_single_numbers(nums):
    xor_all = 0
    for x in nums:
        xor_all ^= x
    low = xor_all & -xor_all
    a = b = 0
    for x in nums:
        if x & low:
            a ^= x
        else:
            b ^= x
    return [min(a, b), max(a, b)]
