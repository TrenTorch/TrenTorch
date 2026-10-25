def subset_sum(nums: list[int], target: int) -> bool:
    """Return True if some subset adds up to target."""

    # This is correct but too slow: it tries taking or skipping every number without remembering results.
    def go(i, rest):
        if rest == 0:
            return True
        if i == len(nums) or rest < 0:
            return False
        return go(i + 1, rest - nums[i]) or go(i + 1, rest)

    return go(0, target)
