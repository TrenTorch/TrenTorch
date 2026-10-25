def min_path_sum(grid):
    rows = len(grid)
    cols = len(grid[0]) if rows else 0
    if rows == 0 or cols == 0:
        return 0
    row = [0] * cols
    for r in range(rows):
        for c in range(cols):
            if r == 0 and c == 0:
                row[c] = grid[0][0]
            elif r == 0:
                row[c] = row[c - 1] + grid[r][c]
            elif c == 0:
                row[c] = row[c] + grid[r][c]
            else:
                row[c] = min(row[c], row[c - 1]) + grid[r][c]
    return row[cols - 1]
