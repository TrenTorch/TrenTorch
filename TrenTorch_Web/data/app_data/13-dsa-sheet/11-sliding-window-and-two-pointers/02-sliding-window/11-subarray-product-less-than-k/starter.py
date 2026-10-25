def count_product_less(nums: list[int], k: int) -> int:
    """Count the subarrays whose product is less than k."""
    # This is correct but too slow: it multiplies out every subarray.
    count = 0
    for i in range(len(nums)):
        product = 1
        for j in range(i, len(nums)):
            product *= nums[j]
            if product >= k:
                break
            count += 1
    return count
