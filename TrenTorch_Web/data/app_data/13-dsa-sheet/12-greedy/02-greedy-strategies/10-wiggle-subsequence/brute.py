def wiggle_length(nums):
    n = len(nums)
    if n == 0:
        return 0
    up = [1] * n
    down = [1] * n
    for i in range(n):
        for j in range(i):
            if nums[i] > nums[j]:
                up[i] = max(up[i], down[j] + 1)
            elif nums[i] < nums[j]:
                down[i] = max(down[i], up[j] + 1)
    return max(max(up), max(down))
