def find_anagrams(s, p):
    m = len(p)
    if m == 0 or m > len(s):
        return []
    need = [0] * 26
    window = [0] * 26
    for ch in p:
        need[ord(ch) - 97] += 1
    out = []
    for i, ch in enumerate(s):
        window[ord(ch) - 97] += 1
        if i >= m:
            window[ord(s[i - m]) - 97] -= 1
        if i >= m - 1 and window == need:
            out.append(i - m + 1)
    return out
