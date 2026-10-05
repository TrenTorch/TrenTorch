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


def add_call_count(function):
    def wrapper(*args, **kwargs):
        wrapper.calls += 1
        return function(*args, **kwargs)

    wrapper.calls = 0
    return wrapper


def run_with_message(function, message: str, *args, **kwargs):
    return function(*args, **kwargs)


def decorate_result(function, prefix: str):
    def wrapper(value):
        return prefix + str(function(value))

    return wrapper
