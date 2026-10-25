def three_sum_closest(nums, target):
    a = sorted(nums)
    best = a[0] + a[1] + a[2]
    for i in range(len(a) - 2):
        lo, hi = i + 1, len(a) - 1
        while lo < hi:
            s = a[i] + a[lo] + a[hi]
            diff = abs(s - target)
            best_diff = abs(best - target)
            if diff < best_diff or (diff == best_diff and s < best):
                best = s
            if s < target:
                lo += 1
            elif s > target:
                hi -= 1
            else:
                return s
    return best
