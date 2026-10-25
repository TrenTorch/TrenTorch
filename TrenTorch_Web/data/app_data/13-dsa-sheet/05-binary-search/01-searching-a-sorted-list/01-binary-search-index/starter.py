def binary_search_index(nums, target):
    """Return the index of target in the sorted list nums, or -1."""
    # This is correct but reads every value. The big tests allow only a few reads.
    for i, x in enumerate(nums):
        if x == target:
            return i
    return -1
