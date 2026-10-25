def total_hamming_distance(nums: list[int]) -> int:
    """Return the sum of the bit differences over all pairs."""
    # This is correct but too slow: it looks at every pair.
    total = 0
    for i in range(len(nums)):
        for j in range(i + 1, len(nums)):
            total += bin(nums[i] ^ nums[j]).count("1")
    return total
