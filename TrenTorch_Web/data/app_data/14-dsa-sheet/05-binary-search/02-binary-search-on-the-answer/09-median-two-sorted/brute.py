def median_two_sorted(a, b):
    merged = sorted(list(a) + list(b))
    n = len(merged)
    if n % 2 == 1:
        return float(merged[n // 2])
    return (merged[n // 2 - 1] + merged[n // 2]) / 2
