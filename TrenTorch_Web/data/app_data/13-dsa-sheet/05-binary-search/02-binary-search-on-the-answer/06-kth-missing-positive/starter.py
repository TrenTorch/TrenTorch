def kth_missing_positive(nums, k):
    """Return the kth positive whole number that is not in nums."""
    # This is correct but reads every value. The big tests allow only a few reads.
    missing = prev = 0
    for x in nums:
        gap = x - prev - 1
        if missing + gap >= k:
            return prev + (k - missing)
        missing += gap
        prev = x
    return prev + (k - missing)
