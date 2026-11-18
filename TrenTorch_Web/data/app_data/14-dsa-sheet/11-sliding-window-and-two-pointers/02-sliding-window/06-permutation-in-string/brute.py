def check_inclusion(s1, s2):
    m = len(s1)
    return any(sorted(s2[i : i + m]) == sorted(s1) for i in range(len(s2) - m + 1))
