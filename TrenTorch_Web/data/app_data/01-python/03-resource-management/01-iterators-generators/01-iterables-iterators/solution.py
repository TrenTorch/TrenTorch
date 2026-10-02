def is_iterator(obj) -> bool:
    return iter(obj) is obj


def get_iterator(iterable):
    return iter(iterable)


def independent_iterators(values: list) -> tuple:
    return (iter(values), iter(values))
