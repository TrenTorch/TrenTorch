def longest_subarray_sum_k_any(nums, k):
    first = {0: -1}
    prefix = best = 0
    for i, x in enumerate(nums):
        prefix += x
        if prefix - k in first:
            best = max(best, i - first[prefix - k])
        if prefix not in first:
            first[prefix] = i
    return best
