def find_needle(haystack: str, needle: str) -> int:
    """Return the first index where needle occurs in haystack, or -1."""
    # This is correct but too slow: it compares the needle letter by letter at every start position.
    n, m = len(haystack), len(needle)
    for i in range(n - m + 1):
        j = 0
        while j < m and haystack[i + j] == needle[j]:
            j += 1
        if j == m:
            return i
    return -1
