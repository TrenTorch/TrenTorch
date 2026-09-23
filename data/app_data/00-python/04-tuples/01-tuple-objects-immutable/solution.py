def make_singleton(x) -> tuple:
    return (x,)


def tuple_replace(t: tuple, index: int, value) -> tuple:
    if index >= len(t) or index < -len(t):
        return t
    if index < 0:
        index += len(t)
    return t[:index] + (value,) + t[index + 1 :]


def count_and_first_index(t: tuple, x) -> tuple:
    if x not in t:
        return (0, -1)
    return (t.count(x), t.index(x))
