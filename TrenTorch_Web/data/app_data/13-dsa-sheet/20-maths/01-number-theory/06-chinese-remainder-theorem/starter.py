def solve_congruences(remainders: list[int], moduli: list[int]) -> int:
    """Return the smallest x >= 0 with x % moduli[i] == remainders[i] for all i, or -1."""
    # This is correct but too slow: it tries the numbers 0, 1, 2, ... one by one.
    from math import lcm

    limit = lcm(*moduli) if moduli else 1
    for x in range(limit):
        if all(x % m == r % m for r, m in zip(remainders, moduli)):
            return x
    return -1
