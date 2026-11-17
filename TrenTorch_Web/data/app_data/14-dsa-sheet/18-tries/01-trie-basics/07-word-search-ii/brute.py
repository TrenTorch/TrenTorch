def find_words(board, words):
    rows = len(board)
    cols = len(board[0]) if rows else 0

    def trace(word):
        def go(r, c, i, used):
            if i == len(word):
                return True
            if (
                not (0 <= r < rows and 0 <= c < cols)
                or (r, c) in used
                or board[r][c] != word[i]
            ):
                return False
            used = used | {(r, c)}
            return (
                go(r + 1, c, i + 1, used)
                or go(r - 1, c, i + 1, used)
                or go(r, c + 1, i + 1, used)
                or go(r, c - 1, i + 1, used)
            )

        return any(go(r, c, 0, frozenset()) for r in range(rows) for c in range(cols))

    return sorted({w for w in words if trace(w)})
