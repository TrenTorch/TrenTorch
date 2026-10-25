def shortest_path_binary_matrix(grid):
    rows = len(grid)
    cols = len(grid[0]) if rows else 0
    if rows == 0 or cols == 0 or grid[0][0] == 1 or grid[rows - 1][cols - 1] == 1:
        return -1
    inf = float("inf")
    dist = [[inf] * cols for _ in range(rows)]
    dist[0][0] = 1
    changed = True
    while changed:
        changed = False
        for r in range(rows):
            for c in range(cols):
                if grid[r][c] == 1:
                    continue
                for dr in (-1, 0, 1):
                    for dc in (-1, 0, 1):
                        nr, nc = r + dr, c + dc
                        if (
                            0 <= nr < rows
                            and 0 <= nc < cols
                            and dist[nr][nc] + 1 < dist[r][c]
                        ):
                            dist[r][c] = dist[nr][nc] + 1
                            changed = True
    return dist[rows - 1][cols - 1] if dist[rows - 1][cols - 1] < inf else -1
