def unique_paths(rows: int, cols: int) -> int:
    """Return the number of paths from the top-left to the bottom-right moving right or down."""
    # This is correct but too slow: it counts the same cells again and again.
    if rows == 1 or cols == 1:
        return 1
    return (unique_paths(rows - 1, cols) + unique_paths(rows, cols - 1)) % (10**9 + 7)
