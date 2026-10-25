def next_greater_circular(nums):
    n = len(nums)
    out = []
    for i in range(n):
        out.append(
            next(
                (nums[(i + k) % n] for k in range(1, n) if nums[(i + k) % n] > nums[i]),
                -1,
            )
        )
    return out
