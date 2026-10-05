def edge_key(a: int, b: int) -> tuple:
    """
    Return a canonical key for an undirected link between `a`
    and `b`: a 2-element tuple with the smaller value first.
    edge_key(a, b) must equal edge_key(b, a).

    Example: edge_key(5, 2) -> (2, 5)
    """
    pass


def count_visits(path: list) -> dict:
    """
    `path` is a list of (x, y) tuples. Return a dictionary that
    maps each distinct (x, y) tuple to the number of times it
    appears in `path`. Use the tuples directly as keys and use
    `in` to check for an existing key.

    Example: count_visits([(0, 0), (1, 0), (0, 0)])
             -> {(0, 0): 2, (1, 0): 1}
    """
    pass


def group_points_by_cell(points: list, cell_size: int) -> dict:
    """
    `points` is a list of (x, y) tuples of ints and `cell_size`
    is a positive int. Return a dictionary mapping each cell
    key (x // cell_size, y // cell_size) to a LIST of the points
    that fall in that cell, in their input order.

    Example: group_points_by_cell([(1, 1), (9, 1), (2, 3)], 5)
             -> {(0, 0): [(1, 1), (2, 3)], (1, 0): [(9, 1)]}
    """
    pass
