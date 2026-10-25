def remove_adjacent_duplicates(s):
    changed = True
    while changed:
        changed = False
        for i in range(len(s) - 1):
            if s[i] == s[i + 1]:
                s = s[:i] + s[i + 2 :]
                changed = True
                break
    return s
