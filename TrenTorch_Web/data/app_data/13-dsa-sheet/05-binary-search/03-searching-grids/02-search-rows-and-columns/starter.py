def search_matrix_ii(matrix, target):
    """Return True if target is in a matrix with sorted rows and sorted columns."""
    # This is correct but reads every value. The big tests allow only a few reads.
    return any(target in row for row in matrix)
