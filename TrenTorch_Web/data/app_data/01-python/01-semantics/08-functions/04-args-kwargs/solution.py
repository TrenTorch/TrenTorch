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
