def count_subset_sums(nums, k, target):
    n = len(nums)
    count = 0
    for mask in range(1 << n):
        if bin(mask).count("1") != k:
            continue
        if sum(nums[i] for i in range(n) if mask >> i & 1) == target:
            count += 1
    return count
