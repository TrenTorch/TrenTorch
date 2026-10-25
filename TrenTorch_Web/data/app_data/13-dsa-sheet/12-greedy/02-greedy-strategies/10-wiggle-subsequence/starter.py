def wiggle_length(nums: list[int]) -> int:
    """Return the length of the longest subsequence whose differences alternate in sign."""
    # This is correct but too slow: for every value it looks at all the earlier values.
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
