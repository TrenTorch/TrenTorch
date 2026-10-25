def kth_largest_stream(k: int, nums: list[int], adds: list[int]) -> list[int]:
    """After each added value, return the kth largest value so far."""
    # This is correct but too slow: it sorts all the values after every addition.
    values = list(nums)
    out = []
    for x in adds:
        values.append(x)
        values.sort(reverse=True)
        out.append(values[k - 1])
    return out
