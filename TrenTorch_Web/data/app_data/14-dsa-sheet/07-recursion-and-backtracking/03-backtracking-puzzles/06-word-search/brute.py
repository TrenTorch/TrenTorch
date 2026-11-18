def word_search(board, word):
    if not word:
        return True
    rows = len(board)
    cols = len(board[0]) if rows else 0

    def paths(r, c, i, used):
        if board[r][c] != word[i]:
            return False
        if i == len(word) - 1:
            return True
        used = used | {(r, c)}
        for dr, dc in ((1, 0), (-1, 0), (0, 1), (0, -1)):
            nr, nc = r + dr, c + dc
            if (
                0 <= nr < rows
                and 0 <= nc < cols
                and (nr, nc) not in used
                and paths(nr, nc, i + 1, used)
            ):
                return True
        return False

    return any(paths(r, c, 0, frozenset()) for r in range(rows) for c in range(cols))
