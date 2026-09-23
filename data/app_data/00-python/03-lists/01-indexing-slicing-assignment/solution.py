def replace_middle(lst: list, new_items: list) -> None:
    if len(lst) < 2:
        return
    lst[1:-1] = new_items


def set_every_other(lst: list, value) -> None:
    lst[::2] = [value] * len(lst[::2])


def slice_copy(lst: list, start: int, stop: int) -> list:
    return lst[start:stop]
