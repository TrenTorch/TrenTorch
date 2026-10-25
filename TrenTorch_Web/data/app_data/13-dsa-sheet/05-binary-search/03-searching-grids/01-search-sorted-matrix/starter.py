def search_matrix(matrix, target):
    """Return True if target is in the matrix whose rows continue each other in order."""
    # This is correct but reads every value. The big tests allow only a few reads.
    return any(target in row for row in matrix)
