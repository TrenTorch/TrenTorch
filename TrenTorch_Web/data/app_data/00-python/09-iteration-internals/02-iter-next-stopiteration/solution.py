def consume_iterator(iterable) -> list:
    iterator = iter(iterable)
    result = []
    while True:
        try:
            result.append(next(iterator))
        except StopIteration:
            break
    return result


def take_first(iterable, count: int) -> list:
    if count <= 0:
        return []
    iterator = iter(iterable)
    result = []
    while len(result) < count:
        try:
            result.append(next(iterator))
        except StopIteration:
            break
    return result


def next_or_default(iterator, default):
    return next(iterator, default)
