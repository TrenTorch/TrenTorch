def sum_of_values(d: dict) -> int:
    return sum(d.values())


def keys_with_max_value(d: dict) -> list:
    if not d:
        return []
    max_value = max(d.values())
    return [key for key, value in d.items() if value == max_value]


def remove_where_value_below(d: dict, threshold: int) -> None:
    for key, value in list(d.items()):
        if value < threshold:
            del d[key]


def value_of(pair: tuple):
    return pair[1]


def items_by_value_desc(d: dict) -> list:
    by_key = sorted(d.items())
    return sorted(by_key, key=value_of, reverse=True)
