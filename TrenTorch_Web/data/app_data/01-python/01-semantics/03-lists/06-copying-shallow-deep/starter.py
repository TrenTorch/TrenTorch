def shallow_copy(lst: list) -> list:
    """
    Return a NEW list object with the same elements as `lst`
    (the elements themselves are shared, not copied). Use the
    copy() method.
    """
    pass


def deep_copy(nested: list) -> list:
    """
    Return a fully independent copy of `nested`: a new list
    whose inner lists (at every depth) are also new objects.
    Use copy.deepcopy (import the copy module at the top of
    your solution).
    """
    pass


def shares_inner_objects(original: list, duplicate: list) -> bool:
    """
    `original` and `duplicate` are lists of equal length. Return
    True if, at every position, the two lists hold the exact
    same object (identity, `is`). Return False if any position
    holds different objects. Two empty lists give True.
    """
    pass


def add_row_safely(matrix: list, row: list) -> list:
    """
    `matrix` is a list of lists. Return a NEW matrix that
    contains independent copies of every row of `matrix` (as
    they were) followed by an independent copy of `row`.
    Neither `matrix` nor `row` (nor any row inside `matrix`)
    may be modified or shared with the returned matrix.
    """
    pass
