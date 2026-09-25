def product(f, lo, hi):
    total = 1
    for i in range(lo, hi + 1):
        total *= f(i)
    return total
