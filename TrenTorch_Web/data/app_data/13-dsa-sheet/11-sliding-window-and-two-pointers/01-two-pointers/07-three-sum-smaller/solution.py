def count_triplets_smaller(nums, target):
    a = sorted(nums)
    count = 0
    for i in range(len(a) - 2):
        lo, hi = i + 1, len(a) - 1
        while lo < hi:
            if a[i] + a[lo] + a[hi] < target:
                count += hi - lo
                lo += 1
            else:
                hi -= 1
    return count
