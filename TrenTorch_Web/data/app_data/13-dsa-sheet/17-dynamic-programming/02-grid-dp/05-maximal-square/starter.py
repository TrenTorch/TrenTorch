def maximal_square(matrix: list[list[int]]) -> int:
    """Return the area of the largest square made only of 1s."""
    # This is correct but too slow: it checks every possible square cell by cell.
    rows = len(matrix)
    cols = len(matrix[0]) if rows else 0
    best = 0
    for r in range(rows):
        for c in range(cols):
            size = 1
            while (
                r + size <= rows
                and c + size <= cols
                and all(
                    matrix[i][j] == 1
                    for i in range(r, r + size)
                    for j in range(c, c + size)
                )
            ):
                best = max(best, size * size)
                size += 1
    return best
