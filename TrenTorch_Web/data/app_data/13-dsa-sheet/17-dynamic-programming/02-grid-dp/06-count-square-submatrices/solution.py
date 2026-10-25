def count_squares(matrix):
    rows = len(matrix)
    cols = len(matrix[0]) if rows else 0
    prev = [0] * (cols + 1)
    total = 0
    for r in range(rows):
        cur = [0] * (cols + 1)
        for c in range(cols):
            if matrix[r][c] == 1:
                cur[c + 1] = 1 + min(prev[c], prev[c + 1], cur[c])
                total += cur[c + 1]
        prev = cur
    return total
