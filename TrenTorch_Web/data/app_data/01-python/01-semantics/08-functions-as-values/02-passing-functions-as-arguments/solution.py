def apply_once(function, value):
    return function(value)


def apply_twice(function, value):
    return function(function(value))


def apply_n_times(function, value, count: int):
    if count <= 0:
        return value
    result = value
    for _ in range(count):
        result = function(result)
    return result


def transform_all(values: list, function) -> list:
    return [function(value) for value in values]
