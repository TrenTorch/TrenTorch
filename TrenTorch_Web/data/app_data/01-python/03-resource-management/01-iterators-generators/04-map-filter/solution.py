def squared(values):
    return map(lambda x: x * x, values)


def keep_positive(values):
    return filter(lambda x: x > 0, values)


def transform_and_filter(values, transform, predicate):
    return filter(predicate, map(transform, values))
