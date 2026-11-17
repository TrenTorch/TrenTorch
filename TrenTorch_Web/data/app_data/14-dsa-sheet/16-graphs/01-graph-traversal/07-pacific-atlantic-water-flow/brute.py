def pacific_atlantic(heights):
    rows = len(heights)
    cols = len(heights[0]) if rows else 0
    out = []
    for r in range(rows):
        for c in range(cols):
            seen = {(r, c)}
            stack = [(r, c)]
            while stack:
                x, y = stack.pop()
                for nx, ny in ((x + 1, y), (x - 1, y), (x, y + 1), (x, y - 1)):
                    if (
                        0 <= nx < rows
                        and 0 <= ny < cols
                        and (nx, ny) not in seen
                        and heights[nx][ny] <= heights[x][y]
                    ):
                        seen.add((nx, ny))
                        stack.append((nx, ny))
            pacific = any(x == 0 or y == 0 for x, y in seen)
            atlantic = any(x == rows - 1 or y == cols - 1 for x, y in seen)
            if pacific and atlantic:
                out.append([r, c])
    return out
