def search_matrix(matrix, target):
    return any(target in row for row in matrix)
