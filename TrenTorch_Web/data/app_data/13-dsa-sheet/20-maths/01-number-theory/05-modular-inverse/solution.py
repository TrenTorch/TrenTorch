def mod_inverse(a, m):
    if m == 1:
        return 0
    old_r, r = a % m, m
    old_x, x = 1, 0
    while r:
        q = old_r // r
        old_r, r = r, old_r - q * r
        old_x, x = x, old_x - q * x
    return old_x % m if old_r == 1 else -1
