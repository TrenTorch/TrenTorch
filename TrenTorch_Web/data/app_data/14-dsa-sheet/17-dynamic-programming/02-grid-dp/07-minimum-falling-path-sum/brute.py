def min_falling_path_sum(matrix):
    if not matrix or not matrix[0]:
        return 0
    rows, cols = len(matrix), len(matrix[0])

    def go(r, c):
        if r == rows - 1:
            return matrix[r][c]
        return matrix[r][c] + min(
            go(r + 1, nc) for nc in (c - 1, c, c + 1) if 0 <= nc < cols
        )

    return min(go(0, c) for c in range(cols))
