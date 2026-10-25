def three_sum(nums):
    """Return all different triples of values that add up to 0."""
    # This is correct but too slow: it tries every set of three positions.
    found = set()
    n = len(nums)
    for i in range(n):
        for j in range(i + 1, n):
            for k in range(j + 1, n):
                if nums[i] + nums[j] + nums[k] == 0:
                    found.add(tuple(sorted((nums[i], nums[j], nums[k]))))
    return [list(t) for t in sorted(found)]
