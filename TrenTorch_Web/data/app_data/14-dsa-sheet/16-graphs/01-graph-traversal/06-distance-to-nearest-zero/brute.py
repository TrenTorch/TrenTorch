def nearest_zero(mat):
    rows = len(mat)
    cols = len(mat[0]) if rows else 0
    zeros = [(r, c) for r in range(rows) for c in range(cols) if mat[r][c] == 0]
    return [
        [
            min((abs(r - zr) + abs(c - zc) for zr, zc in zeros), default=0)
            for c in range(cols)
        ]
        for r in range(rows)
    ]
