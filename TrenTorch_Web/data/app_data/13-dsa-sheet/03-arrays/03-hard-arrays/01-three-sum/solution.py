def three_sum(nums):
    a = sorted(nums)
    out = []
    for i in range(len(a) - 2):
        if i and a[i] == a[i - 1]:
            continue
        lo, hi = i + 1, len(a) - 1
        while lo < hi:
            total = a[i] + a[lo] + a[hi]
            if total < 0:
                lo += 1
            elif total > 0:
                hi -= 1
            else:
                out.append([a[i], a[lo], a[hi]])
                lo += 1
                hi -= 1
                while lo < hi and a[lo] == a[lo - 1]:
                    lo += 1
                while lo < hi and a[hi] == a[hi + 1]:
                    hi -= 1
    return out
