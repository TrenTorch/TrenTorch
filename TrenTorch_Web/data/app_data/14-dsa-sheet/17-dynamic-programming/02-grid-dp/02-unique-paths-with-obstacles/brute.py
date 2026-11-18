def unique_paths_obstacles(grid):
    rows = len(grid)
    cols = len(grid[0]) if rows else 0
    if rows == 0 or cols == 0:
        return 0

    def go(r, c):
        if r >= rows or c >= cols or grid[r][c] == 1:
            return 0
        if r == rows - 1 and c == cols - 1:
            return 1
        return go(r + 1, c) + go(r, c + 1)

    return go(0, 0) % (10**9 + 7)
