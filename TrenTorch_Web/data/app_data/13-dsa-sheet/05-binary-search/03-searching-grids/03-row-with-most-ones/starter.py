def row_with_most_ones(matrix):
    """Return the index of the row with the most 1s, or -1."""
    # This is correct but reads every value. The big tests allow only a few reads.
    best_row, best = -1, 0
    for i, row in enumerate(matrix):
        if sum(row) > best:
            best_row, best = i, sum(row)
    return best_row
