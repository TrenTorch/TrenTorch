def largest_island(grid):
    rows = len(grid)
    cols = len(grid[0]) if rows else 0

    def biggest(g):
        seen = set()
        best = 0
        for r in range(rows):
            for c in range(cols):
                if g[r][c] == 1 and (r, c) not in seen:
                    seen.add((r, c))
                    stack = [(r, c)]
                    count = 0
                    while stack:
                        x, y = stack.pop()
                        count += 1
                        for nx, ny in ((x + 1, y), (x - 1, y), (x, y + 1), (x, y - 1)):
                            if (
                                0 <= nx < rows
                                and 0 <= ny < cols
                                and g[nx][ny] == 1
                                and (nx, ny) not in seen
                            ):
                                seen.add((nx, ny))
                                stack.append((nx, ny))
                    best = max(best, count)
        return best

    best = biggest(grid)
    for r in range(rows):
        for c in range(cols):
            if grid[r][c] == 0:
                g = [row[:] for row in grid]
                g[r][c] = 1
                best = max(best, biggest(g))
    return best
