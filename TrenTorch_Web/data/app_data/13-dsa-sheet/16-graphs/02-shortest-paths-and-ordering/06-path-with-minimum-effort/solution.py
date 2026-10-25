import heapq


def minimum_effort_path(heights):
    rows, cols = len(heights), len(heights[0])
    inf = float("inf")
    effort = [[inf] * cols for _ in range(rows)]
    effort[0][0] = 0
    heap = [(0, 0, 0)]
    while heap:
        e, x, y = heapq.heappop(heap)
        if x == rows - 1 and y == cols - 1:
            return e
        if e > effort[x][y]:
            continue
        for nx, ny in ((x + 1, y), (x - 1, y), (x, y + 1), (x, y - 1)):
            if 0 <= nx < rows and 0 <= ny < cols:
                ne = max(e, abs(heights[nx][ny] - heights[x][y]))
                if ne < effort[nx][ny]:
                    effort[nx][ny] = ne
                    heapq.heappush(heap, (ne, nx, ny))
    return 0
