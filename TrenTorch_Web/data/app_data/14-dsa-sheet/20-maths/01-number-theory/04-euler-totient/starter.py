from math import gcd


def euler_phi(n: int) -> int:
    """Return how many numbers from 1 to n have no common factor with n."""
    # This is correct but too slow: it computes a gcd for every number up to n.
    return sum(1 for k in range(1, n + 1) if gcd(k, n) == 1)
