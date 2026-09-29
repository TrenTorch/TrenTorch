def power(x, exponent=2):
    return x**exponent


def make_label(value, prefix="item"):
    return f"{prefix}:{value}"


def append_value(value, items=None):
    if items is None:
        items = []
    items.append(value)
    return items


def describe_config(name, enabled=True, retries=3):
    return (name, enabled, retries)
