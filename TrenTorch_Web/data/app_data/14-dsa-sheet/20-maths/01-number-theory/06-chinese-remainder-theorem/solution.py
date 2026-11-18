from math import gcd


def solve_congruences(remainders, moduli):
    x, modulus = 0, 1
    for r, m in zip(remainders, moduli):
        g = gcd(modulus, m)
        if (r - x) % g:
            return -1
        lcm = modulus // g * m
        t = ((r - x) // g * pow(modulus // g, -1, m // g)) % (m // g)
        x = (x + modulus * t) % lcm
        modulus = lcm
    return x
