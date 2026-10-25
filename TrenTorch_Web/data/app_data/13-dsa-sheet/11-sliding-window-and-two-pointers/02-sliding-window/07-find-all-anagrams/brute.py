def find_anagrams(s, p):
    m = len(p)
    if m == 0:
        return []
    return [i for i in range(len(s) - m + 1) if sorted(s[i : i + m]) == sorted(p)]
