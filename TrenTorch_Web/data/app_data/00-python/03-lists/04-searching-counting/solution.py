def index_or_minus_one(lst: list, value) -> int:
    try:
        return lst.index(value)
    except ValueError:
        return -1


def all_indices(lst: list, value) -> list:
    return [i for i, x in enumerate(lst) if x == value]


def contains_all(lst: list, needles: list) -> bool:
    return all(needle in lst for needle in needles)


def contains_same_object(lst: list, target) -> bool:
    return any(x is target for x in lst)
