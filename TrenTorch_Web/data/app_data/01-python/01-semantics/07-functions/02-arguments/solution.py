def build_point(x, y):
    return (x, y)


def configure_model(name, dimensions, metric):
    return {"name": name, "dimensions": dimensions, "metric": metric}


def format_record(identifier, value, label):
    return f"{identifier}={value} [{label}]"


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


def sum_all(*values):
    total = 0
    for value in values:
        total += value
    return total


def collect_types(*values):
    return tuple(type(value) for value in values)


def build_options(**options):
    return dict(options)


def summarize(required, *values, **options):
    return {"required": required, "values": values, "options": options}


def call_with_options(function, args, options):
    return function(*args, **options)
