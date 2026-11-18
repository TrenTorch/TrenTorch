def valid_sudoku(board):
    seen = set()
    for r in range(9):
        for c in range(9):
            digit = board[r][c]
            if digit == 0:
                continue
            keys = (
                ("row", r, digit),
                ("col", c, digit),
                ("box", (r // 3) * 3 + c // 3, digit),
            )
            if any(key in seen for key in keys):
                return False
            seen.update(keys)
    return True
