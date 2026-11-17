def valid_sudoku(board):
    groups = []
    for i in range(9):
        groups.append([board[i][j] for j in range(9)])
        groups.append([board[j][i] for j in range(9)])
        groups.append(
            [
                board[3 * (i // 3) + a][3 * (i % 3) + b]
                for a in range(3)
                for b in range(3)
            ]
        )
    for group in groups:
        digits = [x for x in group if x != 0]
        if len(digits) != len(set(digits)):
            return False
    return True
