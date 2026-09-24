def nested_get(d: dict, path: list, default):
    current = d
    for key in path:
        if not isinstance(current, dict) or key not in current:
            return default
        current = current[key]
    return current


def nested_set(d: dict, path: list, value) -> None:
    current = d
    for key in path[:-1]:
        if key not in current or not isinstance(current[key], dict):
            current[key] = {}
        current = current[key]
    current[path[-1]] = value


def flatten_two_levels(d: dict) -> dict:
    result = {}
    for outer_key, inner in d.items():
        for inner_key, value in inner.items():
            result[f"{outer_key}.{inner_key}"] = value
    return result
