def kth_smallest_matrix(matrix, k):
    return sorted(x for row in matrix for x in row)[k - 1]
