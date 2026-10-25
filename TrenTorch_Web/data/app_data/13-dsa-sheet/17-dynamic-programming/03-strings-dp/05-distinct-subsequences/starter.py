def num_distinct(s: str, t: str) -> int:
    """Count the ways to form t as a subsequence of s, modulo 10**9 + 7."""

    # This is correct but too slow: it solves the same pairs of positions again and again.
    def go(i, j):
        if j == len(t):
            return 1
        if i == len(s):
            return 0
        total = go(i + 1, j)
        if s[i] == t[j]:
            total += go(i + 1, j + 1)
        return total

    return go(0, 0) % (10**9 + 7)
