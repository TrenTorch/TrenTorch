def longest_substring_k_repeating(s, k):
    best = 0
    for i in range(len(s)):
        for j in range(i + 1, len(s) + 1):
            part = s[i:j]
            if all(part.count(ch) >= k for ch in set(part)):
                best = max(best, j - i)
    return best
