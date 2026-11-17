def min_insertions(s):
    def go(i, j):
        if i >= j:
            return 0
        if s[i] == s[j]:
            return go(i + 1, j - 1)
        return 1 + min(go(i + 1, j), go(i, j - 1))

    return go(0, len(s) - 1)
