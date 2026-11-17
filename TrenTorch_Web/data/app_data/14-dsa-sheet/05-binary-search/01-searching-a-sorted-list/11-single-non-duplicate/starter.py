def single_non_duplicate(nums):
    """Return the value that appears once; every other value appears twice."""
    # This is correct but reads every value. The big tests allow only a few reads.
    result = 0
    for x in nums:
        result ^= x
    return result
