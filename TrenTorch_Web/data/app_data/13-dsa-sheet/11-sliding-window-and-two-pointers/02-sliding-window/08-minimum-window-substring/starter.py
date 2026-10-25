def min_window(s: str, t: str) -> str:
    """Return the smallest substring of s that contains every character of t."""
    # This is correct but too slow: it checks every substring from scratch.
    if not t:
        return ""
    need = {}
    for ch in t:
        need[ch] = need.get(ch, 0) + 1
    best = ""
    for i in range(len(s)):
        have = {}
        missing = len(need)
        for j in range(i, len(s)):
            have[s[j]] = have.get(s[j], 0) + 1
            if s[j] in need and have[s[j]] == need[s[j]]:
                missing -= 1
            if missing == 0:
                if best == "" or j - i + 1 < len(best):
                    best = s[i : j + 1]
                break
    return best
