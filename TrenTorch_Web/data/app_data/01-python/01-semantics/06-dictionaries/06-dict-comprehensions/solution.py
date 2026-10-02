def square_map(n: int) -> dict:
    if n < 1:
        return {}
    return {i: i * i for i in range(1, n + 1)}


def invert(d: dict) -> dict:
    return {value: key for key, value in d.items()}


def filter_items(d: dict, min_value: int) -> dict:
    return {key: value for key, value in d.items() if value >= min_value}


def dict_from_parallel(keys: list, values: list) -> dict:
    return {key: value for key, value in zip(keys, values)}
