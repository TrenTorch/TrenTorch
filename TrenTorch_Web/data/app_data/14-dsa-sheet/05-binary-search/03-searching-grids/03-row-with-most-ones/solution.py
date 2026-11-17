def row_with_most_ones(matrix):
    best_row = -1
    col = len(matrix[0]) if matrix else 0
    for i, row in enumerate(matrix):
        moved = False
        while col > 0 and row[col - 1] == 1:
            col -= 1
            moved = True
        if moved:
            best_row = i
    return best_row
