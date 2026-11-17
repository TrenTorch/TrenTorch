def word_search(board, word):
    if not word:
        return True
    rows = len(board)
    cols = len(board[0]) if rows else 0
    grid = [list(row) for row in board]

    def go(r, c, i):
        if i == len(word):
            return True
        if not (0 <= r < rows and 0 <= c < cols) or grid[r][c] != word[i]:
            return False
        saved = grid[r][c]
        grid[r][c] = "#"
        found = (
            go(r + 1, c, i + 1)
            or go(r - 1, c, i + 1)
            or go(r, c + 1, i + 1)
            or go(r, c - 1, i + 1)
        )
        grid[r][c] = saved
        return found

    return any(go(r, c, 0) for r in range(rows) for c in range(cols))
