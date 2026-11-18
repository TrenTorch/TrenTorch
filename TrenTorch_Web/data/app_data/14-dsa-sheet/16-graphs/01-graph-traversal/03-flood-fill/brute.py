def flood_fill(image, sr, sc, color):
    rows, cols = len(image), len(image[0])
    old = image[sr][sc]
    reach = {(sr, sc)}
    changed = True
    while changed:
        changed = False
        for x, y in list(reach):
            for nx, ny in ((x + 1, y), (x - 1, y), (x, y + 1), (x, y - 1)):
                if (
                    0 <= nx < rows
                    and 0 <= ny < cols
                    and image[nx][ny] == old
                    and (nx, ny) not in reach
                ):
                    reach.add((nx, ny))
                    changed = True
    return [
        [color if (r, c) in reach else image[r][c] for c in range(cols)]
        for r in range(rows)
    ]
