def rat_in_a_maze(maze):
    rows = len(maze)
    cols = len(maze[0]) if rows else 0
    if rows == 0 or cols == 0 or maze[0][0] == 0 or maze[rows - 1][cols - 1] == 0:
        return []
    out = []
    path = []
    on_path = [[False] * cols for _ in range(rows)]
    moves = (("D", 1, 0), ("L", 0, -1), ("R", 0, 1), ("U", -1, 0))

    def go(r, c):
        if r == rows - 1 and c == cols - 1:
            out.append("".join(path))
            return
        on_path[r][c] = True
        for letter, dr, dc in moves:
            nr, nc = r + dr, c + dc
            if (
                0 <= nr < rows
                and 0 <= nc < cols
                and maze[nr][nc] == 1
                and not on_path[nr][nc]
            ):
                path.append(letter)
                go(nr, nc)
                path.pop()
        on_path[r][c] = False

    go(0, 0)
    return out
