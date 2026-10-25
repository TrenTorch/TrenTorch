def range_minimums(nums: list[int], queries: list[list[int]]) -> list[int]:
    """Answer each range minimum query [l, r]."""
    # This is correct but too slow: every query looks at the whole range again.
    return [min(nums[left : right + 1]) for left, right in queries]
