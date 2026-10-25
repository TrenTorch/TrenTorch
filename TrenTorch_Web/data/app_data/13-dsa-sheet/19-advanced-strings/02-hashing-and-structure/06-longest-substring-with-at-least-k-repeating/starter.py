def longest_substring_k_repeating(s: str, k: int) -> int:
    """Return the length of the longest substring in which every letter appears at least k times."""
    # This is correct but too slow: it counts the letters of every substring.
    best = 0
    for i in range(len(s)):
        counts = {}
        for j in range(i, len(s)):
            counts[s[j]] = counts.get(s[j], 0) + 1
            if all(c >= k for c in counts.values()):
                best = max(best, j - i + 1)
    return best
