def rotate_matrix(matrix):
    return [list(column) for column in zip(*matrix[::-1])]
