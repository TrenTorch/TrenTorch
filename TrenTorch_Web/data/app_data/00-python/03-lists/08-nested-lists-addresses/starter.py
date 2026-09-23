def make_grid(rows: int, cols: int, fill) -> list:
    """
    Return a NEW list of `rows` lists, each containing `cols`
    copies of `fill`. Every row must be a separate list object,
    so mutating one row never changes another. If rows or cols
    is 0 (or negative), return the matching empty structure
    (rows <= 0 -> []; cols <= 0 -> a list of empty rows).
    Use a comprehension.

    Example: make_grid(2, 3, 0) -> [[0, 0, 0], [0, 0, 0]]
    """
    pass


def rows_are_independent(grid: list) -> bool:
    """
    Return True if every row of `grid` (a list of lists) is a
    distinct object, i.e. no two rows have the same id().
    A grid with 0 or 1 rows returns True.
    """
    pass


def transpose(matrix: list) -> list:
    """
    `matrix` is a non-empty rectangular list of lists. Return
    a NEW matrix in which rows and columns are swapped. The
    input must not be modified, and the result's rows must be
    new list objects.

    Example: transpose([[1, 2, 3], [4, 5, 6]])
             -> [[1, 4], [2, 5], [3, 6]]
    """
    pass
