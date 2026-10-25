def max_sum_k(nums: list[int], k: int) -> int:
    """Return the largest sum of k consecutive values."""
    # This is correct but too slow: it adds up every window from scratch.
    return max(sum(nums[i : i + k]) for i in range(len(nums) - k + 1))
