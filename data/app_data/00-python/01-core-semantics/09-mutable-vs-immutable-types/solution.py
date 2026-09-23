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
