def search_matrix_ii(matrix, target):
    return any(target in row for row in matrix)
