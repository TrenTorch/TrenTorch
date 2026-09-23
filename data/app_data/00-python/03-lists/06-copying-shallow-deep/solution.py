import copy


def shallow_copy(lst: list) -> list:
    return lst.copy()


def deep_copy(nested: list) -> list:
    return copy.deepcopy(nested)


def shares_inner_objects(original: list, duplicate: list) -> bool:
    return all(a is b for a, b in zip(original, duplicate))


def add_row_safely(matrix: list, row: list) -> list:
    new_matrix = [copy.deepcopy(existing_row) for existing_row in matrix]
    new_matrix.append(copy.deepcopy(row))
    return new_matrix
