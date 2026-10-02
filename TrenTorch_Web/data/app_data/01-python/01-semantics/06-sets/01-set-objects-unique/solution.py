def unique_values(values) -> set:
    return set(values)


def contains_all(values, candidates) -> bool:
    value_set = set(values)
    return all(candidate in value_set for candidate in candidates)


def unique_count(values) -> int:
    return len(set(values))
