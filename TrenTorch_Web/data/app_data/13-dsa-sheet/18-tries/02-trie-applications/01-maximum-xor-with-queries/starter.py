def max_xor_queries(nums: list[int], queries: list[int]) -> list[int]:
    """For each query x, return the largest x ^ n over the numbers n."""
    # This is correct but too slow: it tries every number for every query.
    return [max(x ^ n for n in nums) for x in queries]
