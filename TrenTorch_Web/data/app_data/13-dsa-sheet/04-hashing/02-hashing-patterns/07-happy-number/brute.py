def happy_number(n):
    for _ in range(1000):
        if n == 1:
            return True
        n = sum(int(ch) ** 2 for ch in str(n))
    return n == 1
