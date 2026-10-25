def rat_in_a_maze(maze):
    rows = len(maze)
    cols = len(maze[0]) if rows else 0
    if rows == 0 or cols == 0 or maze[0][0] == 0 or maze[rows - 1][cols - 1] == 0:
        return []
    found = []

    def walk(r, c, seen, path):
        if (r, c) == (rows - 1, cols - 1):
            found.append(path)
            return
        for letter, dr, dc in (("U", -1, 0), ("R", 0, 1), ("L", 0, -1), ("D", 1, 0)):
            nr, nc = r + dr, c + dc
            if (
                0 <= nr < rows
                and 0 <= nc < cols
                and maze[nr][nc] == 1
                and (nr, nc) not in seen
            ):
                walk(nr, nc, seen | {(nr, nc)}, path + letter)

    walk(0, 0, {(0, 0)}, "")
    return sorted(found)
