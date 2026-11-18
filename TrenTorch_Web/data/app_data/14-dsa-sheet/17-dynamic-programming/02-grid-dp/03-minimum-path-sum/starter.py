def min_path_sum(grid: list[list[int]]) -> int:
    """Return the smallest sum on a path from the top-left to the bottom-right moving right or down."""
    # This is correct but too slow: it solves the same cells again and again.
    rows, cols = len(grid), len(grid[0]) if grid else 0

    def go(r, c):
        if r == rows - 1 and c == cols - 1:
            return grid[r][c]
        best = float("inf")
        if r + 1 < rows:
            best = min(best, go(r + 1, c))
        if c + 1 < cols:
            best = min(best, go(r, c + 1))
        return grid[r][c] + best

    return go(0, 0) if rows and cols else 0
