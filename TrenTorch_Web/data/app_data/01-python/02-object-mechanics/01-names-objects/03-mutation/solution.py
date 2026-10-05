def mutate_list(lst: list) -> None:
    lst.append(4)


def reassign_list(lst: list) -> list:
    return [9, 9, 9]


def observe_through_alias(original: list) -> dict:
    alias = original
    original.append(100)
    alias_after_mutation = list(alias)
    original = [0, 0, 0]
    alias_after_reassignment = list(alias)
    return {
        "alias_after_mutation": alias_after_mutation,
        "alias_after_reassignment": alias_after_reassignment,
        "original_final": original,
    }


_IMMUTABLE_TYPES = (int, float, bool, str, tuple, frozenset)


def is_mutable_type(value) -> bool:
    return not isinstance(value, _IMMUTABLE_TYPES)


def tuple_inner_mutation_check(t: tuple) -> dict:
    tuple_id_before = id(t)
    t[0].append(100)
    return {
        "tuple_id_before": tuple_id_before,
        "tuple_id_after": id(t),
        "inner_list_after": list(t[0]),
    }
