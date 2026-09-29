def combine_sets(a: set, b: set) -> set:
    return a | b


def common_values(a: set, b: set) -> set:
    return a & b


def only_in_first(a: set, b: set) -> set:
    return a - b


def in_exactly_one(a: set, b: set) -> set:
    return a ^ b


def relationship(a: set, b: set) -> tuple:
    return (a.issubset(b), a.issuperset(b), a.isdisjoint(b))
