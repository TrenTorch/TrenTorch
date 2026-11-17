def character_replacement(s, k):
    count = {}
    left = 0
    max_count = 0
    for right, ch in enumerate(s):
        count[ch] = count.get(ch, 0) + 1
        max_count = max(max_count, count[ch])
        if right - left + 1 - max_count > k:
            count[s[left]] -= 1
            left += 1
    return len(s) - left
