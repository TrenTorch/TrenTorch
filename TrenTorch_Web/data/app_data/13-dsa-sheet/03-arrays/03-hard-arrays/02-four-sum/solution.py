def four_sum(nums, target):
    a = sorted(nums)
    n = len(a)
    out = []
    for i in range(n - 3):
        if i and a[i] == a[i - 1]:
            continue
        for j in range(i + 1, n - 2):
            if j > i + 1 and a[j] == a[j - 1]:
                continue
            lo, hi = j + 1, n - 1
            while lo < hi:
                total = a[i] + a[j] + a[lo] + a[hi]
                if total < target:
                    lo += 1
                elif total > target:
                    hi -= 1
                else:
                    out.append([a[i], a[j], a[lo], a[hi]])
                    lo += 1
                    hi -= 1
                    while lo < hi and a[lo] == a[lo - 1]:
                        lo += 1
                    while lo < hi and a[hi] == a[hi + 1]:
                        hi -= 1
    return out
