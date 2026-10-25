def subset_sum(nums, target):
    sums = {0}
    for x in nums:
        sums |= {s + x for s in sums}
    return target in sums
