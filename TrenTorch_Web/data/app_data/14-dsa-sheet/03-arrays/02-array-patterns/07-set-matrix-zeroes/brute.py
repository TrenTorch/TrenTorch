def set_matrix_zeroes(matrix):
    result = [list(row) for row in matrix]
    for i in range(len(matrix)):
        for j in range(len(matrix[i])):
            if matrix[i][j] == 0:
                for k in range(len(matrix[i])):
                    result[i][k] = 0
                for k in range(len(matrix)):
                    result[k][j] = 0
    return result
