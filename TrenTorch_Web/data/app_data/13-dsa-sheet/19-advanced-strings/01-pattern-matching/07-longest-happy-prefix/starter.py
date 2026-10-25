def longest_happy_prefix(s: str) -> str:
    """Return the longest proper prefix that is also a suffix."""
    # This is correct but too slow: it compares every possible length from scratch.
    for length in range(len(s) - 1, 0, -1):
        if all(s[i] == s[len(s) - length + i] for i in range(length)):
            return s[:length]
    return ""
