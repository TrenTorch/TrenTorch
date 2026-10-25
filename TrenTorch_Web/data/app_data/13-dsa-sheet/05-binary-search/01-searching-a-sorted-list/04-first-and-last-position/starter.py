def first_and_last(nums, target):
    """Return [first index, last index] of target, or [-1, -1]."""
    # This is correct but reads every value. The big tests allow only a few reads.
    found = [i for i, x in enumerate(nums) if x == target]
    return [found[0], found[-1]] if found else [-1, -1]
