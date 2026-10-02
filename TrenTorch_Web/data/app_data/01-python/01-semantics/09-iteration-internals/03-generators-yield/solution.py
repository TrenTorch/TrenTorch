def generate_range(start: int, stop: int):
    value = start
    while value < stop:
        yield value
        value += 1


def generate_squares(values):
    for value in values:
        yield value * value


def generate_until(values, limit):
    for value in values:
        if value > limit:
            return
        yield value
