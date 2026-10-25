def max_xor_pair(nums: list[int]) -> int:
    """Return the largest a ^ b over two numbers of the list."""
    # This is correct but too slow: it tries every pair.
    best = 0
    for i in range(len(nums)):
        for j in range(i + 1, len(nums)):
            best = max(best, nums[i] ^ nums[j])
    return best
