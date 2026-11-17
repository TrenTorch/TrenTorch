def count_product_less(nums, k):
    product = 1
    left = 0
    total = 0
    for right, x in enumerate(nums):
        product *= x
        while left <= right and product >= k:
            product //= nums[left]
            left += 1
        total += right - left + 1
    return total
