def num_islands(grid):
    rows = len(grid)
    cols = len(grid[0]) if rows else 0
    parent = {}

    def find(a):
        while parent[a] != a:
            parent[a] = parent[parent[a]]
            a = parent[a]
        return a

    for r in range(rows):
        for c in range(cols):
            if grid[r][c] == 1:
                parent[(r, c)] = (r, c)
    for r, c in list(parent):
        for nxt in ((r + 1, c), (r, c + 1)):
            if nxt in parent:
                parent[find((r, c))] = find(nxt)
    return len({find(cell) for cell in parent})
