def min_path_sum(grid):
    rows = len(grid)
    cols = len(grid[0]) if rows else 0
    if rows == 0 or cols == 0:
        return 0

    def go(r, c):
        if r == rows - 1 and c == cols - 1:
            return grid[r][c]
        options = []
        if r + 1 < rows:
            options.append(go(r + 1, c))
        if c + 1 < cols:
            options.append(go(r, c + 1))
        return grid[r][c] + min(options)

    return go(0, 0)
