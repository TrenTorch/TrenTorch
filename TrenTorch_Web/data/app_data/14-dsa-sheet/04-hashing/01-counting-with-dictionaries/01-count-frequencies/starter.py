def count_frequencies(nums, queries):
    """For each query value, return how many times it appears in nums."""
    # This is correct but too slow: it counts again from scratch for every query.
    return [nums.count(q) for q in queries]
