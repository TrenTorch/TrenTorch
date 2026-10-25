def min_jumps(nums):
    n = len(nums)
    if n <= 1:
        return 0
    jumps = 0
    end = far = 0
    for i in range(n - 1):
        far = max(far, i + nums[i])
        if i == far:
            return -1
        if i == end:
            jumps += 1
            end = far
            if end >= n - 1:
                break
    return jumps if end >= n - 1 else -1
