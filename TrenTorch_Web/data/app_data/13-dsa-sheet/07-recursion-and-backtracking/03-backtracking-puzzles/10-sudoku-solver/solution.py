def sudoku_solver(board):
    grid = [list(row) for row in board]
    rows = [set() for _ in range(9)]
    cols = [set() for _ in range(9)]
    boxes = [set() for _ in range(9)]
    empty = []
    for r in range(9):
        for c in range(9):
            v = grid[r][c]
            if v:
                rows[r].add(v)
                cols[c].add(v)
                boxes[r // 3 * 3 + c // 3].add(v)
            else:
                empty.append((r, c))

    def candidates(r, c):
        return (
            {1, 2, 3, 4, 5, 6, 7, 8, 9} - rows[r] - cols[c] - boxes[r // 3 * 3 + c // 3]
        )

    def go():
        best = None
        for r, c in empty:
            if grid[r][c] == 0:
                options = candidates(r, c)
                if best is None or len(options) < len(best[2]):
                    best = (r, c, options)
                    if len(options) <= 1:
                        break
        if best is None:
            return True
        r, c, options = best
        for v in sorted(options):
            grid[r][c] = v
            rows[r].add(v)
            cols[c].add(v)
            boxes[r // 3 * 3 + c // 3].add(v)
            if go():
                return True
            grid[r][c] = 0
            rows[r].discard(v)
            cols[c].discard(v)
            boxes[r // 3 * 3 + c // 3].discard(v)
        return False

    go()
    return grid
