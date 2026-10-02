def find_duplicates(values: list) -> set:
    seen = set()
    duplicates = set()
    for value in values:
        if value in seen:
            duplicates.add(value)
        else:
            seen.add(value)
    return duplicates


def unique_in_first_seen_order(values: list) -> list:
    seen = set()
    result = []
    for value in values:
        if value not in seen:
            seen.add(value)
            result.append(value)
    return result


def all_seen_before(values: list) -> bool:
    counts = {}
    for value in values:
        counts[value] = counts.get(value, 0) + 1
    return all(count != 1 for count in counts.values())


def missing_values(values: list, expected: set) -> set:
    return expected - set(values)
