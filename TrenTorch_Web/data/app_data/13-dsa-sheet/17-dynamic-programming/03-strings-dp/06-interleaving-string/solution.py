def is_interleave(a, b, c):
    if len(a) + len(b) != len(c):
        return False
    row = [False] * (len(b) + 1)
    row[0] = True
    for j in range(1, len(b) + 1):
        row[j] = row[j - 1] and b[j - 1] == c[j - 1]
    for i in range(1, len(a) + 1):
        row[0] = row[0] and a[i - 1] == c[i - 1]
        for j in range(1, len(b) + 1):
            row[j] = (row[j] and a[i - 1] == c[i + j - 1]) or (
                row[j - 1] and b[j - 1] == c[i + j - 1]
            )
    return row[len(b)]
