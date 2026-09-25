def remove_keys(d: dict, keys: list) -> int:
    removed = 0
    for key in keys:
        if key in d:
            del d[key]
            removed += 1
    return removed


def take_last(d: dict):
    if not d:
        return None
    return d.popitem()


def remove_and_return(d: dict, key, default):
    return d.pop(key, default)


def clear_and_report(d: dict) -> int:
    count = len(d)
    d.clear()
    return count
