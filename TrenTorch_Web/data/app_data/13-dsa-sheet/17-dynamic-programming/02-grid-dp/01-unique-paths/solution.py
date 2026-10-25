def unique_paths(rows, cols):
    mod = 10**9 + 7
    row = [1] * cols
    for _ in range(1, rows):
        for c in range(1, cols):
            row[c] = (row[c] + row[c - 1]) % mod
    return row[cols - 1]
