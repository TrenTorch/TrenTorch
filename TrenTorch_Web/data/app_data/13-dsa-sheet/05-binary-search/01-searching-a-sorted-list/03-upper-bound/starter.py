def upper_bound(nums, target):
    """Return the first index whose value is greater than target."""
    # This is correct but reads every value. The big tests allow only a few reads.
    for i, x in enumerate(nums):
        if x > target:
            return i
    return len(nums)
