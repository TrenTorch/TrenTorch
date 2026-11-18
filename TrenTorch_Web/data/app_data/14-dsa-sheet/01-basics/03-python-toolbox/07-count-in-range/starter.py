def count_in_range(sorted_nums, queries):
    """For each [lo, hi], count the values v with lo <= v <= hi."""
    # This is correct but too slow: it scans the whole list for every query.
    return [sum(1 for v in sorted_nums if lo <= v <= hi) for lo, hi in queries]
