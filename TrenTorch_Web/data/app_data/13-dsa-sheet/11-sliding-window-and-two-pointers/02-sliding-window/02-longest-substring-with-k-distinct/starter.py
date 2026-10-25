def longest_k_distinct(s: str, k: int) -> int:
    """Return the length of the longest substring with at most k different characters."""
    # This is correct but too slow: it tries every start and extends until there are too many characters.
    best = 0
    for i in range(len(s)):
        seen = set()
        for j in range(i, len(s)):
            seen.add(s[j])
            if len(seen) > k:
                break
            best = max(best, j - i + 1)
    return best
