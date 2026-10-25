import heapq


def swim_in_water(grid):
    n, m = len(grid), len(grid[0])
    seen = [[False] * m for _ in range(n)]
    heap = [(grid[0][0], 0, 0)]
    seen[0][0] = True
    while heap:
        t, x, y = heapq.heappop(heap)
        if x == n - 1 and y == m - 1:
            return t
        for nx, ny in ((x + 1, y), (x - 1, y), (x, y + 1), (x, y - 1)):
            if 0 <= nx < n and 0 <= ny < m and not seen[nx][ny]:
                seen[nx][ny] = True
                heapq.heappush(heap, (max(t, grid[nx][ny]), nx, ny))
    return 0
