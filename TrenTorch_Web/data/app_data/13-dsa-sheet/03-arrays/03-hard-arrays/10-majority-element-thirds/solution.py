def majority_element_thirds(nums):
    a = b = None
    ca = cb = 0
    for x in nums:
        if x == a:
            ca += 1
        elif x == b:
            cb += 1
        elif ca == 0:
            a, ca = x, 1
        elif cb == 0:
            b, cb = x, 1
        else:
            ca -= 1
            cb -= 1
    n = len(nums)
    return sorted(v for v in {a, b} if v is not None and nums.count(v) * 3 > n)
