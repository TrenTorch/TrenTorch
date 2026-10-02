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
