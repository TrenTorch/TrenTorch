def sum_subarray_mins(arr: list[int]) -> int:
    """Return the sum of the minimum of every subarray, modulo 10**9 + 7."""
    # This is correct but too slow: it visits every subarray.
    total = 0
    for i in range(len(arr)):
        lowest = arr[i]
        for j in range(i, len(arr)):
            lowest = min(lowest, arr[j])
            total += lowest
    return total % (10**9 + 7)
