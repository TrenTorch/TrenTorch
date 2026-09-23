def freeze_rows(matrix: list) -> tuple:
    return tuple(tuple(row) for row in matrix)


def thaw_rows(frozen: tuple) -> list:
    return [list(row) for row in frozen]


def updated(seq, index: int, value):
    is_tuple = isinstance(seq, tuple)
    items = list(seq)
    try:
        items[index] = value
    except IndexError:
        pass
    return tuple(items) if is_tuple else items


def has_mutable_element(t: tuple) -> bool:
    return any(isinstance(x, (list, dict, set)) for x in t)
