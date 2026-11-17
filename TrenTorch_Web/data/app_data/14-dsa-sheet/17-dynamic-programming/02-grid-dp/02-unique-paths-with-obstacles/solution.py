def unique_paths_obstacles(grid):
    rows = len(grid)
    cols = len(grid[0]) if rows else 0
    if rows == 0 or cols == 0:
        return 0
    mod = 10**9 + 7
    row = [0] * cols
    row[0] = 1 if grid[0][0] == 0 else 0
    for r in range(rows):
        for c in range(cols):
            if grid[r][c] == 1:
                row[c] = 0
            elif c > 0:
                row[c] = (row[c] + row[c - 1]) % mod
    return row[cols - 1]
