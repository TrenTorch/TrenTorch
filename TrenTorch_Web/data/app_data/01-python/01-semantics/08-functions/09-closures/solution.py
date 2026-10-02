def make_multiplier(factor):
    def multiply(value):
        return value * factor

    return multiply


def make_prefixer(prefix: str):
    def add_prefix(text):
        return prefix + text

    return add_prefix


def make_counter(start: int):
    count = start

    def next_count():
        nonlocal count
        count += 1
        return count

    return next_count
