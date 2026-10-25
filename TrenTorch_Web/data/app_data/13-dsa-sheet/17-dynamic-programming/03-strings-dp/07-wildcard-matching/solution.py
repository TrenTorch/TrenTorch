def is_match_wildcard(s, p):
    prev = [False] * (len(p) + 1)
    prev[0] = True
    for j in range(1, len(p) + 1):
        prev[j] = prev[j - 1] and p[j - 1] == "*"
    for i in range(1, len(s) + 1):
        cur = [False] * (len(p) + 1)
        for j in range(1, len(p) + 1):
            if p[j - 1] == "*":
                cur[j] = cur[j - 1] or prev[j]
            elif p[j - 1] == "?" or p[j - 1] == s[i - 1]:
                cur[j] = prev[j - 1]
        prev = cur
    return prev[len(p)]
