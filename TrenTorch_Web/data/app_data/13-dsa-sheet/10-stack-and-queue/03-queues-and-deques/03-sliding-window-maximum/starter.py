def sliding_window_max(nums: list[int], k: int) -> list[int]:
    """Return the maximum of every window of k consecutive values."""
    # This is correct but too slow: it scans every window completely.
    return [max(nums[i : i + k]) for i in range(len(nums) - k + 1)]
