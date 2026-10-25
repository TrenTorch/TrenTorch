def sum_divisor_counts(n):
    return sum(sum(1 for j in range(1, k + 1) if k % j == 0) for k in range(1, n + 1))
