def power_mod(base: int, exp: int, mod: int) -> int:
    """Return base to the power exp, taken modulo mod."""
    # This is correct but too slow: it multiplies exp times.
    result = 1 % mod
    for _ in range(exp):
        result = result * base % mod
    return result
