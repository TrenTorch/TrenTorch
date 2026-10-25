def rotation_count(nums):
    """Return how many places a sorted list was rotated."""
    # This is correct but reads every value. The big tests allow only a few reads.
    return nums.index(min(nums))
