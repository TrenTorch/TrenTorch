def alias_and_call(function, value):
    alias = function
    return alias(value)


def apply_selected(functions: list, index: int, value):
    selected = functions[index]
    return selected(value)


def same_function(function_a, function_b) -> bool:
    return function_a is function_b
