def can_partition(nums):
    total = sum(nums)
    if total % 2:
        return False
    sums = {0}
    for x in nums:
        sums |= {s + x for s in sums}
    return total // 2 in sums
