def is_match_wildcard(s, p):
    def go(i, j):
        if j == len(p):
            return i == len(s)
        if p[j] == "*":
            return any(go(k, j + 1) for k in range(i, len(s) + 1))
        return i < len(s) and (p[j] == "?" or p[j] == s[i]) and go(i + 1, j + 1)

    return go(0, 0)
