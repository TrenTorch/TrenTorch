def longest_k_distinct(s, k):
    count = {}
    left = 0
    best = 0
    for right, ch in enumerate(s):
        count[ch] = count.get(ch, 0) + 1
        while len(count) > k:
            count[s[left]] -= 1
            if count[s[left]] == 0:
                del count[s[left]]
            left += 1
        best = max(best, right - left + 1)
    return best
