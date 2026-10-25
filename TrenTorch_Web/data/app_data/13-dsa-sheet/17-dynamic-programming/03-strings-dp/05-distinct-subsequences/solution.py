def num_distinct(s, t):
    mod = 10**9 + 7
    row = [1] + [0] * len(t)
    for ch in s:
        for j in range(len(t), 0, -1):
            if t[j - 1] == ch:
                row[j] = (row[j] + row[j - 1]) % mod
    return row[len(t)]
