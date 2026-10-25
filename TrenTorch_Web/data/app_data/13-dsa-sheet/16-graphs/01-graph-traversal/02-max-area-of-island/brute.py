def max_island_area(grid):
    rows = len(grid)
    cols = len(grid[0]) if rows else 0
    best = 0
    for r in range(rows):
        for c in range(cols):
            if grid[r][c] != 1:
                continue
            reach = {(r, c)}
            changed = True
            while changed:
                changed = False
                for x, y in list(reach):
                    for nx, ny in ((x + 1, y), (x - 1, y), (x, y + 1), (x, y - 1)):
                        if (
                            0 <= nx < rows
                            and 0 <= ny < cols
                            and grid[nx][ny] == 1
                            and (nx, ny) not in reach
                        ):
                            reach.add((nx, ny))
                            changed = True
            best = max(best, len(reach))
    return best
