def swim_in_water(grid):
    n, m = len(grid), len(grid[0])
    for t in range(n * m):
        if grid[0][0] > t:
            continue
        seen = {(0, 0)}
        stack = [(0, 0)]
        while stack:
            x, y = stack.pop()
            for nx, ny in ((x + 1, y), (x - 1, y), (x, y + 1), (x, y - 1)):
                if (
                    0 <= nx < n
                    and 0 <= ny < m
                    and (nx, ny) not in seen
                    and grid[nx][ny] <= t
                ):
                    seen.add((nx, ny))
                    stack.append((nx, ny))
        if (n - 1, m - 1) in seen:
            return t
    return 0
