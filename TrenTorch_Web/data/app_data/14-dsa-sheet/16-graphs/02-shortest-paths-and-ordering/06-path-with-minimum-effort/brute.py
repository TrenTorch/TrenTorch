def minimum_effort_path(heights):
    rows, cols = len(heights), len(heights[0])
    inf = float("inf")
    effort = [[inf] * cols for _ in range(rows)]
    effort[0][0] = 0
    changed = True
    while changed:
        changed = False
        for x in range(rows):
            for y in range(cols):
                for nx, ny in ((x + 1, y), (x - 1, y), (x, y + 1), (x, y - 1)):
                    if 0 <= nx < rows and 0 <= ny < cols:
                        ne = max(effort[nx][ny], abs(heights[nx][ny] - heights[x][y]))
                        if ne < effort[x][y]:
                            effort[x][y] = ne
                            changed = True
    return effort[rows - 1][cols - 1]
