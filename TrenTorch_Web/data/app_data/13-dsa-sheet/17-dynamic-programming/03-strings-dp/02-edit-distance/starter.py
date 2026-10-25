def edit_distance(a: str, b: str) -> int:
    """Return the fewest insertions, deletions and replacements that turn a into b."""

    # This is correct but too slow: it solves the same pairs of prefixes again and again.
    def go(i, j):
        if i == len(a):
            return len(b) - j
        if j == len(b):
            return len(a) - i
        if a[i] == b[j]:
            return go(i + 1, j + 1)
        return 1 + min(go(i + 1, j), go(i, j + 1), go(i + 1, j + 1))

    return go(0, 0)
