def check_inclusion(s1, s2):
    m = len(s1)
    if m > len(s2):
        return False
    need = [0] * 26
    window = [0] * 26
    for ch in s1:
        need[ord(ch) - 97] += 1
    for i, ch in enumerate(s2):
        window[ord(ch) - 97] += 1
        if i >= m:
            window[ord(s2[i - m]) - 97] -= 1
        if i >= m - 1 and window == need:
            return True
    return m == 0
