def largest_island(grid):
    rows = len(grid)
    cols = len(grid[0]) if rows else 0
    label = [[0] * cols for _ in range(rows)]
    size = {}
    next_id = 1
    for r in range(rows):
        for c in range(cols):
            if grid[r][c] == 1 and label[r][c] == 0:
                label[r][c] = next_id
                stack = [(r, c)]
                count = 0
                while stack:
                    x, y = stack.pop()
                    count += 1
                    for nx, ny in ((x + 1, y), (x - 1, y), (x, y + 1), (x, y - 1)):
                        if (
                            0 <= nx < rows
                            and 0 <= ny < cols
                            and grid[nx][ny] == 1
                            and label[nx][ny] == 0
                        ):
                            label[nx][ny] = next_id
                            stack.append((nx, ny))
                size[next_id] = count
                next_id += 1
    best = max(size.values(), default=0)
    for r in range(rows):
        for c in range(cols):
            if grid[r][c] == 0:
                around = set()
                for nx, ny in ((r + 1, c), (r - 1, c), (r, c + 1), (r, c - 1)):
                    if 0 <= nx < rows and 0 <= ny < cols and label[nx][ny]:
                        around.add(label[nx][ny])
                best = max(best, 1 + sum(size[i] for i in around))
    return best
