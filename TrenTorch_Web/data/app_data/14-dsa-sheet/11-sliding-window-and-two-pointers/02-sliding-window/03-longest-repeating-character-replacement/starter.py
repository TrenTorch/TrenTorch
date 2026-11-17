def character_replacement(s: str, k: int) -> int:
    """Return the longest run you can make by changing at most k characters."""
    # This is correct but too slow: it counts the letters of every substring from scratch.
    best = 0
    for i in range(len(s)):
        for j in range(i, len(s)):
            part = s[i : j + 1]
            if len(part) - max(part.count(c) for c in set(part)) <= k:
                best = max(best, len(part))
    return best
