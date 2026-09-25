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
