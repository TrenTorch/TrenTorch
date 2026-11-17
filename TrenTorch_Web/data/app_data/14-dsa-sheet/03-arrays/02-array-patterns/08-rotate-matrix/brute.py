def rotate_matrix(matrix):
    m = len(matrix)
    if m == 0 or len(matrix[0]) == 0:
        return []
    n = len(matrix[0])
    result = [[0] * m for _ in range(n)]
    for i in range(m):
        for j in range(n):
            result[j][m - 1 - i] = matrix[i][j]
    return result
