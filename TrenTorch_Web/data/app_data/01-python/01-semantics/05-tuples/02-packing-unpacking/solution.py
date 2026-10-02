def rotate_three(a, b, c) -> tuple:
    a, b, c = b, c, a
    return (a, b, c)


def head_and_tail(seq) -> tuple:
    if len(seq) == 0:
        return (None, [])
    head, *tail = seq
    return (head, tail)


def ends_and_middle(seq) -> tuple:
    first, *middle, last = seq
    return (first, middle, last)


def sum_pairs(pairs: list) -> list:
    return [a + b for a, b in pairs]
