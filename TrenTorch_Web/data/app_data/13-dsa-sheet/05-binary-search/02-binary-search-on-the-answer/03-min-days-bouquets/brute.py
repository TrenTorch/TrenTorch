def min_days_bouquets(bloom, m, k):
    if m * k > len(bloom):
        return -1
    for day in sorted(set(bloom)):
        bouquets = run = 0
        for b in bloom:
            if b <= day:
                run += 1
                if run == k:
                    bouquets += 1
                    run = 0
            else:
                run = 0
        if bouquets >= m:
            return day
