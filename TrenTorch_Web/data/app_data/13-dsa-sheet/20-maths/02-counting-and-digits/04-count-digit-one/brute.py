def count_digit_one(n):
    return sum(str(k).count("1") for k in range(1, n + 1))
