def row_with_most_ones(matrix):
    best_row, best = -1, 0
    for i, row in enumerate(matrix):
        if sum(row) > best:
            best_row, best = i, sum(row)
    return best_row
