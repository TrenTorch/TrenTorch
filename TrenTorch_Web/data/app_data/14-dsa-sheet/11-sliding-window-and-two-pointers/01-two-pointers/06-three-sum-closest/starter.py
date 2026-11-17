def three_sum_closest(nums: list[int], target: int) -> int:
    """Return the sum of three values that is closest to target."""
    # This is correct but too slow: it tries every triple.
    best = None
    for i in range(len(nums)):
        for j in range(i + 1, len(nums)):
            for k in range(j + 1, len(nums)):
                total = nums[i] + nums[j] + nums[k]
                if best is None or (abs(total - target), total) < (
                    abs(best - target),
                    best,
                ):
                    best = total
    return best
