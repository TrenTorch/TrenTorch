from math import lcm


def solve_congruences(remainders, moduli):
    limit = lcm(*moduli) if moduli else 1
    for x in range(limit):
        if all(x % m == r % m for r, m in zip(remainders, moduli)):
            return x
    return -1
