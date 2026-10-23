from collections import deque


def oranges_rotting(grid):
    rows = len(grid)
    cols = len(grid[0]) if rows else 0
    g = [row[:] for row in grid]
    queue = deque()
    fresh = 0
    for r in range(rows):
        for c in range(cols):
            if g[r][c] == 2:
                queue.append((r, c))
            elif g[r][c] == 1:
                fresh += 1
    minutes = 0
    while queue and fresh:
        minutes += 1
        for _ in range(len(queue)):
            x, y = queue.popleft()
            for nx, ny in ((x + 1, y), (x - 1, y), (x, y + 1), (x, y - 1)):
                if 0 <= nx < rows and 0 <= ny < cols and g[nx][ny] == 1:
                    g[nx][ny] = 2
                    fresh -= 1
                    queue.append((nx, ny))
    return minutes if fresh == 0 else -1
