def lcs_length(a: str, b: str) -> int:
    """Return the length of the longest common subsequence."""

    # This is correct but too slow: it solves the same pairs of prefixes again and again.
    def go(i, j):
        if i == len(a) or j == len(b):
            return 0
        if a[i] == b[j]:
            return 1 + go(i + 1, j + 1)
        return max(go(i + 1, j), go(i, j + 1))

    return go(0, 0)
