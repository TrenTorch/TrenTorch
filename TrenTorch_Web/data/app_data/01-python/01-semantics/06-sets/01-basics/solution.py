def unique_values(values) -> set:
    return set(values)


def contains_all(values, candidates) -> bool:
    value_set = set(values)
    return all(candidate in value_set for candidate in candidates)


def unique_count(values) -> int:
    return len(set(values))


def add_values(values, additions) -> set:
    result = set(values)
    for item in additions:
        result.add(item)
    return result


def remove_if_present(values: set, value) -> set:
    values.discard(value)
    return values


def remove_required(values: set, value) -> set:
    values.remove(value)
    return values


def empty_set(values: set) -> set:
    values.clear()
    return values
