def longest_zero_sum_subarray(nums):
    first = {0: -1}
    prefix = best = 0
    for i, x in enumerate(nums):
        prefix += x
        if prefix in first:
            best = max(best, i - first[prefix])
        else:
            first[prefix] = i
    return best
