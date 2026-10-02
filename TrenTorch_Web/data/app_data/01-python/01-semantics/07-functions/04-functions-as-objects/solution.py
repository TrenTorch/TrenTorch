def alias_and_call(function, value):
    alias = function
    return alias(value)


def apply_selected(functions: list, index: int, value):
    selected = functions[index]
    return selected(value)


def same_function(function_a, function_b) -> bool:
    return function_a is function_b


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


def make_square_function():
    return lambda x: x * x


def make_offset_function(offset):
    return lambda x: x + offset


def apply_lambda(values: list, function) -> list:
    return [function(value) for value in values]
