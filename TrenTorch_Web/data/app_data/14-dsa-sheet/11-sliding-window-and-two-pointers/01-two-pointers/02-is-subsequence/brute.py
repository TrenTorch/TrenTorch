def is_subsequence(s, t):
    pos = -1
    for ch in s:
        pos = t.find(ch, pos + 1)
        if pos == -1:
            return False
    return True
