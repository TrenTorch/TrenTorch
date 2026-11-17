def subarrays_divisible_by_k(nums, k):
    seen = {0: 1}
    prefix = count = 0
    for x in nums:
        prefix = (prefix + x) % k
        count += seen.get(prefix, 0)
        seen[prefix] = seen.get(prefix, 0) + 1
    return count
