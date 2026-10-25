def min_insertions(s):
    n = len(s)
    if n == 0:
        return 0
    prev = [0] * n
    for i in range(n - 1, -1, -1):
        cur = [0] * n
        cur[i] = 1
        for j in range(i + 1, n):
            if s[i] == s[j]:
                cur[j] = 2 + prev[j - 1]
            else:
                cur[j] = max(prev[j], cur[j - 1])
        prev = cur
    return n - prev[n - 1]
