def did_mutate_in_place(lst: list, operation) -> bool:
    before = id(lst)
    result = operation(lst)
    if result is not None:
        lst = result
    after = id(lst)
    return before == after


def are_same_object(a, b) -> bool:
    return a is b
