def count_divisor_steps(n):
    count = 0
    for i in range(1, n + 1):
        for j in range(i, n + 1, i):
            count += 1
    return count
