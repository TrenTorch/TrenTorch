def min_window(s, t):
    if not t:
        return ""
    need = {}
    for ch in t:
        need[ch] = need.get(ch, 0) + 1
    have = {}
    missing = len(need)
    best_start, best_len = 0, len(s) + 1
    left = 0
    for right, ch in enumerate(s):
        have[ch] = have.get(ch, 0) + 1
        if ch in need and have[ch] == need[ch]:
            missing -= 1
        while missing == 0:
            if right - left + 1 < best_len:
                best_start, best_len = left, right - left + 1
            gone = s[left]
            have[gone] -= 1
            if gone in need and have[gone] < need[gone]:
                missing += 1
            left += 1
    return s[best_start : best_start + best_len] if best_len <= len(s) else ""
