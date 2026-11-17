def palindrome_partitions(s):
    n = len(s)
    pal = [[False] * n for _ in range(n)]
    for length in range(1, n + 1):
        for i in range(n - length + 1):
            j = i + length - 1
            pal[i][j] = s[i] == s[j] and (length <= 2 or pal[i + 1][j - 1])
    out = []

    def go(start, pieces):
        if start == n:
            out.append(list(pieces))
            return
        for j in range(start, n):
            if pal[start][j]:
                pieces.append(s[start : j + 1])
                go(j + 1, pieces)
                pieces.pop()

    go(0, [])
    return out
