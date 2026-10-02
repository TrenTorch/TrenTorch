def make_grid(rows: int, cols: int, fill) -> list:
    if rows <= 0:
        return []
    if cols <= 0:
        return [[] for _ in range(rows)]
    return [[fill for _ in range(cols)] for _ in range(rows)]


def rows_are_independent(grid: list) -> bool:
    ids = [id(row) for row in grid]
    return len(ids) == len(set(ids))


def transpose(matrix: list) -> list:
    num_rows = len(matrix)
    num_cols = len(matrix[0])
    return [[matrix[i][j] for i in range(num_rows)] for j in range(num_cols)]
