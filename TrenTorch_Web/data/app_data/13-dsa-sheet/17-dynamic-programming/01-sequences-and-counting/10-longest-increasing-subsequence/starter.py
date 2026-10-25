def length_of_lis(nums: list[int]) -> int:
    """Return the length of the longest strictly increasing subsequence."""
    # This is correct but too slow: it compares every value with all the earlier ones.
    best = [1] * len(nums)
    for i in range(len(nums)):
        for j in range(i):
            if nums[j] < nums[i] and best[j] + 1 > best[i]:
                best[i] = best[j] + 1
    return max(best, default=0)
