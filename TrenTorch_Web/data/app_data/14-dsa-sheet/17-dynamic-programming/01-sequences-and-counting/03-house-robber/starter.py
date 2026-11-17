def rob(nums: list[int]) -> int:
    """Return the most money you can take without robbing two neighbouring houses."""

    # This is correct but too slow: it tries both choices for every house without remembering results.
    def go(i):
        if i >= len(nums):
            return 0
        return max(nums[i] + go(i + 2), go(i + 1))

    return go(0)
