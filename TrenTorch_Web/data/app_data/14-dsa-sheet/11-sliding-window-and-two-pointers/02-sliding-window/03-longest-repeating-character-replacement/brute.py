def character_replacement(s, k):
    best = 0
    for i in range(len(s)):
        for j in range(i, len(s)):
            part = s[i : j + 1]
            if len(part) - max(part.count(c) for c in set(part)) <= k:
                best = max(best, len(part))
    return best
