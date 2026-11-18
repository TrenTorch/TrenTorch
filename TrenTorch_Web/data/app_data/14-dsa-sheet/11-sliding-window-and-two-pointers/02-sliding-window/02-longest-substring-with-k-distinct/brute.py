def longest_k_distinct(s, k):
    best = 0
    for i in range(len(s)):
        for j in range(i, len(s)):
            if len(set(s[i : j + 1])) <= k:
                best = max(best, j - i + 1)
    return best
