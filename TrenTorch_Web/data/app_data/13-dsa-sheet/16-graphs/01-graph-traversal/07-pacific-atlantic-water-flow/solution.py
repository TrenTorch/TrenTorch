def pacific_atlantic(heights):
    rows = len(heights)
    cols = len(heights[0]) if rows else 0

    def flood(starts):
        seen = set(starts)
        stack = list(starts)
        while stack:
            x, y = stack.pop()
            for nx, ny in ((x + 1, y), (x - 1, y), (x, y + 1), (x, y - 1)):
                if (
                    0 <= nx < rows
                    and 0 <= ny < cols
                    and (nx, ny) not in seen
                    and heights[nx][ny] >= heights[x][y]
                ):
                    seen.add((nx, ny))
                    stack.append((nx, ny))
        return seen

    pacific = flood([(r, 0) for r in range(rows)] + [(0, c) for c in range(cols)])
    atlantic = flood(
        [(r, cols - 1) for r in range(rows)] + [(rows - 1, c) for c in range(cols)]
    )
    return [list(cell) for cell in sorted(pacific & atlantic)]
