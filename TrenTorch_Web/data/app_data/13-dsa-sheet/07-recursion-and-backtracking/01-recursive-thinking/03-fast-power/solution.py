def power_mod(base, exp, mod):
    result = 1 % mod
    base %= mod
    while exp:
        if exp & 1:
            result = result * base % mod
        base = base * base % mod
        exp >>= 1
    return result
