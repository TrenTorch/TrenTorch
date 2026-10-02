def make_square_function():
    return lambda x: x * x


def make_offset_function(offset):
    return lambda x: x + offset


def apply_lambda(values: list, function) -> list:
    return [function(value) for value in values]
