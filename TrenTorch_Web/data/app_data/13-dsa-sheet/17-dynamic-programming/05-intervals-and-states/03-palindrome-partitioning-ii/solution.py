def min_cut_palindromes(s):
    n = len(s)
    if n == 0:
        return 0
    pal = [[False] * n for _ in range(n)]
    for i in range(n - 1, -1, -1):
        for j in range(i, n):
            if s[i] == s[j] and (j - i < 2 or pal[i + 1][j - 1]):
                pal[i][j] = True
    cuts = [0] * n
    for j in range(n):
        if pal[0][j]:
            cuts[j] = 0
            continue
        best = j
        for i in range(1, j + 1):
            if pal[i][j] and cuts[i - 1] + 1 < best:
                best = cuts[i - 1] + 1
        cuts[j] = best
    return cuts[n - 1]
