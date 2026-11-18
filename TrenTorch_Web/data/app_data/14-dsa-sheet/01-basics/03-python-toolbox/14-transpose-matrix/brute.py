def transpose_matrix(matrix):
    if not matrix or not matrix[0]:
        return []
    return [[matrix[i][j] for i in range(len(matrix))] for j in range(len(matrix[0]))]
