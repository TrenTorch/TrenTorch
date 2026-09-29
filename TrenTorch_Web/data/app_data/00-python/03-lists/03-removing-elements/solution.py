def remove_all(lst: list, value) -> None:
    kept = [x for x in lst if x != value]
    lst[:] = kept


def pop_last_n(lst: list, n: int) -> list:
    if n <= 0:
        return []
    if n > len(lst):
        n = len(lst)
    removed = lst[-n:]
    del lst[-n:]
    return removed


def delete_every_other(lst: list) -> None:
    del lst[::2]


def remove_first_or_report(lst: list, value) -> bool:
    if value in lst:
        lst.remove(value)
        return True
    return False
