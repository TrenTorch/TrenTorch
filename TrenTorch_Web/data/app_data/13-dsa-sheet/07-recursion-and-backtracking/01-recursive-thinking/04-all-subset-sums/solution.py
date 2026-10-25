def all_subset_sums(nums):
    sums = [0]
    for x in nums:
        sums += [s + x for s in sums]
    return sorted(sums)
