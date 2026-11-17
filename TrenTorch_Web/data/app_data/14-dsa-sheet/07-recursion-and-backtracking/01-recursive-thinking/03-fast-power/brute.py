def power_mod(base, exp, mod):
    result = 1 % mod
    for _ in range(exp):
        result = result * base % mod
    return result
