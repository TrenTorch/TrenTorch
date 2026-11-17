def mod_inverse(a, m):
    return next((x for x in range(m) if a * x % m == 1 % m), -1)
