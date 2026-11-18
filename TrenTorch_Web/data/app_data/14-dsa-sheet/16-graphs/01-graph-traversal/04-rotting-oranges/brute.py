def oranges_rotting(grid):
    g = [row[:] for row in grid]
    rows = len(g)
    cols = len(g[0]) if rows else 0
    minutes = 0
    while True:
        fresh = [(r, c) for r in range(rows) for c in range(cols) if g[r][c] == 1]
        if not fresh:
            return minutes
        spreading = [
            (r, c)
            for r, c in fresh
            if any(
                0 <= r + dr < rows and 0 <= c + dc < cols and g[r + dr][c + dc] == 2
                for dr, dc in ((1, 0), (-1, 0), (0, 1), (0, -1))
            )
        ]
        if not spreading:
            return -1
        for r, c in spreading:
            g[r][c] = 2
        minutes += 1
