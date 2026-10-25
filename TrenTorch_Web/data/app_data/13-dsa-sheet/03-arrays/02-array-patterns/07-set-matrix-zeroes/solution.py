def set_matrix_zeroes(matrix):
    rows = {i for i, row in enumerate(matrix) if 0 in row}
    cols = {j for row in matrix for j, x in enumerate(row) if x == 0}
    return [
        [0 if i in rows or j in cols else x for j, x in enumerate(row)]
        for i, row in enumerate(matrix)
    ]
