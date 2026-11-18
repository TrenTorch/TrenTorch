def count_doubling_steps(n):
    count = 0
    i = 1
    while i < n:
        i *= 2
        count += 1
    return count
