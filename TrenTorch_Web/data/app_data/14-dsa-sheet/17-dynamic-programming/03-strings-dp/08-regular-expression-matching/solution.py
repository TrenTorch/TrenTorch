def is_match_regex(s, p):
    def fits(x, ch):
        return x == "." or x == ch

    prev = [False] * (len(p) + 1)
    prev[0] = True
    for j in range(2, len(p) + 1):
        prev[j] = p[j - 1] == "*" and prev[j - 2]
    for i in range(1, len(s) + 1):
        cur = [False] * (len(p) + 1)
        for j in range(1, len(p) + 1):
            if p[j - 1] == "*":
                cur[j] = cur[j - 2] or (fits(p[j - 2], s[i - 1]) and prev[j])
            else:
                cur[j] = fits(p[j - 1], s[i - 1]) and prev[j - 1]
        prev = cur
    return prev[len(p)]
