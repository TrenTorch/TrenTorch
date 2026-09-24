COUNTER = 0


def local_double(value):
    result = value * 2
    return result


def read_limit(value, limit):
    return value <= limit


def increment_global():
    global COUNTER
    COUNTER = COUNTER + 1
    return COUNTER


def mutate_shared(items, value):
    items.append(value)
    return items
