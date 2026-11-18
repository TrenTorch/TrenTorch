def longest_unique_substring(s):
    """Return the length of the longest substring with all different characters."""
    # This is correct but too slow: it restarts from every position.
    best = 0
    for i in range(len(s)):
        seen = set()
        for j in range(i, len(s)):
            if s[j] in seen:
                break
            seen.add(s[j])
        best = max(best, len(seen))
    return best
