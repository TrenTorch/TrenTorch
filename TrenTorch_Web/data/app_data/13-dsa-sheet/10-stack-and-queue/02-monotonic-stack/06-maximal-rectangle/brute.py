def maximal_rectangle(matrix):
    rows = len(matrix)
    cols = len(matrix[0]) if rows else 0
    best = 0
    for r1 in range(rows):
        for r2 in range(r1, rows):
            for c1 in range(cols):
                for c2 in range(c1, cols):
                    if all(
                        matrix[r][c]
                        for r in range(r1, r2 + 1)
                        for c in range(c1, c2 + 1)
                    ):
                        best = max(best, (r2 - r1 + 1) * (c2 - c1 + 1))
    return best
