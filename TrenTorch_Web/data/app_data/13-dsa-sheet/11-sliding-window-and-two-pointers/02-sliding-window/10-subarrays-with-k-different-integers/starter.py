def subarrays_k_distinct(nums: list[int], k: int) -> int:
    """Count the subarrays that have exactly k different values."""
    # This is correct but too slow: it looks at every subarray.
    count = 0
    for i in range(len(nums)):
        seen = set()
        for j in range(i, len(nums)):
            seen.add(nums[j])
            if len(seen) == k:
                count += 1
            elif len(seen) > k:
                break
    return count
