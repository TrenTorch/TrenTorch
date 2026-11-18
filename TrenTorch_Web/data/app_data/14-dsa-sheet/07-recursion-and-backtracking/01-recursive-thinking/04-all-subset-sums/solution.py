def all_subset_sums(nums):
    sums = [0]
    for x in nums:
        # both halves are sorted, so Timsort merges them in linear time
        sums = sorted(sums + [s + x for s in sums])
    return sums
