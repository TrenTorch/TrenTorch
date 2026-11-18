def common_values(a, b):
    """Return the sorted different values that appear in both lists."""
    # This is correct but too slow: `in` on a list is a linear search.
    return sorted({x for x in a if x in b})
