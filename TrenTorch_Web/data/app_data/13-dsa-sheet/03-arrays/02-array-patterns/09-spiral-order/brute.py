def spiral_order(matrix):
    if not matrix or not matrix[0]:
        return []
    rows, cols = len(matrix), len(matrix[0])
    seen = [[False] * cols for _ in range(rows)]
    directions = [(0, 1), (1, 0), (0, -1), (-1, 0)]
    i = j = d = 0
    out = []
    for _ in range(rows * cols):
        out.append(matrix[i][j])
        seen[i][j] = True
        ni, nj = i + directions[d][0], j + directions[d][1]
        if not (0 <= ni < rows and 0 <= nj < cols and not seen[ni][nj]):
            d = (d + 1) % 4
            ni, nj = i + directions[d][0], j + directions[d][1]
        i, j = ni, nj
    return out
