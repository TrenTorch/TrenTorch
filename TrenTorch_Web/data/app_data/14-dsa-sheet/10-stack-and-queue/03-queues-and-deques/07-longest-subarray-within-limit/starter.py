def longest_within_limit(nums: list[int], limit: int) -> int:
    """Return the longest subarray whose largest and smallest values differ by at most limit."""
    # This is correct but too slow: it recomputes the largest and smallest of every window.
    best = 0
    left = 0
    for right in range(len(nums)):
        while max(nums[left : right + 1]) - min(nums[left : right + 1]) > limit:
            left += 1
        best = max(best, right - left + 1)
    return best
