def eager_double(values) -> list:
    return [x * 2 for x in values]


def lazy_double(values):
    return (x * 2 for x in values)


def lazy_positive(values):
    return (x for x in values if x > 0)
