def longest_repeated_length(s: str) -> int:
    """Return the length of the longest substring that occurs at least twice."""
    # This is correct but too slow: it tries every length, longest first, and builds every substring of that length.
    for length in range(len(s) - 1, 0, -1):
        seen = set()
        for i in range(len(s) - length + 1):
            part = s[i : i + length]
            if part in seen:
                return length
            seen.add(part)
    return 0
