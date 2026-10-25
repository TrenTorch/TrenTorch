def number_of_subarrays(nums: list[int], k: int) -> int:
    """Count the subarrays that contain exactly k odd numbers."""
    # This is correct but too slow: it counts the odd numbers of every subarray.
    count = 0
    for i in range(len(nums)):
        odd = 0
        for j in range(i, len(nums)):
            odd += nums[j] % 2
            if odd == k:
                count += 1
            elif odd > k:
                break
    return count
