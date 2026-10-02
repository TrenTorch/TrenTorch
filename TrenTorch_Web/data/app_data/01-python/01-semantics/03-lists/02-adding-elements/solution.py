def append_all(lst: list, items: list) -> None:
    lst.extend(items)


def insert_sorted(lst: list, value) -> None:
    i = 0
    while i < len(lst) and lst[i] <= value:
        i += 1
    lst.insert(i, value)


def flatten_one_level(list_of_lists: list) -> list:
    result = []
    for inner in list_of_lists:
        result.extend(inner)
    return result


def concat_identity_report(lst: list, extra: list) -> list:
    id_before = id(lst)
    lst += extra
    same_after_iadd = id(lst) == id_before

    id_before_plus = id(lst)
    lst = lst + extra
    same_after_plus = id(lst) == id_before_plus

    return [same_after_iadd, same_after_plus]
