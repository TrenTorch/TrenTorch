def max_island_area(grid):
    rows = len(grid)
    cols = len(grid[0]) if rows else 0
    seen = [[False] * cols for _ in range(rows)]
    best = 0
    for r in range(rows):
        for c in range(cols):
            if grid[r][c] == 1 and not seen[r][c]:
                seen[r][c] = True
                stack = [(r, c)]
                size = 0
                while stack:
                    x, y = stack.pop()
                    size += 1
                    for nx, ny in ((x + 1, y), (x - 1, y), (x, y + 1), (x, y - 1)):
                        if (
                            0 <= nx < rows
                            and 0 <= ny < cols
                            and grid[nx][ny] == 1
                            and not seen[nx][ny]
                        ):
                            seen[nx][ny] = True
                            stack.append((nx, ny))
                best = max(best, size)
    return best
