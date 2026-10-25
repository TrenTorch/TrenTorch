from collections import deque


def shortest_path_binary_matrix(grid):
    rows = len(grid)
    cols = len(grid[0]) if rows else 0
    if rows == 0 or cols == 0 or grid[0][0] == 1 or grid[rows - 1][cols - 1] == 1:
        return -1
    seen = [[False] * cols for _ in range(rows)]
    seen[0][0] = True
    queue = deque([(0, 0, 1)])
    while queue:
        x, y, steps = queue.popleft()
        if x == rows - 1 and y == cols - 1:
            return steps
        for dx in (-1, 0, 1):
            for dy in (-1, 0, 1):
                nx, ny = x + dx, y + dy
                if (
                    0 <= nx < rows
                    and 0 <= ny < cols
                    and grid[nx][ny] == 0
                    and not seen[nx][ny]
                ):
                    seen[nx][ny] = True
                    queue.append((nx, ny, steps + 1))
    return -1
