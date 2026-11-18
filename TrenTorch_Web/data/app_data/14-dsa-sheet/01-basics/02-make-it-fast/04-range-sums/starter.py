def range_sums(nums, queries):
    """Return the sum of nums[l..r] for each [l, r] in queries."""
    # This is correct but too slow: it re-adds every range from scratch.
    return [sum(nums[left : right + 1]) for left, right in queries]
