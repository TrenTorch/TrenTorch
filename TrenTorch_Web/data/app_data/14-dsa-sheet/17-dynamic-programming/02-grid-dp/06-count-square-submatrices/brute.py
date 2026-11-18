def count_squares(matrix):
    rows = len(matrix)
    cols = len(matrix[0]) if rows else 0
    total = 0
    for r in range(rows):
        for c in range(cols):
            size = 1
            while r + size <= rows and c + size <= cols:
                if all(
                    matrix[i][j] == 1
                    for i in range(r, r + size)
                    for j in range(c, c + size)
                ):
                    total += 1
                size += 1
    return total
