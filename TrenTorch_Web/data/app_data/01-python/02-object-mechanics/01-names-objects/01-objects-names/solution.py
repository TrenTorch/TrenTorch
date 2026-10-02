def describe_object(value) -> dict:
    return {"type": type(value).__name__, "address": id(value)}


def same_object(var1_value, var2_value) -> bool:
    return id(var1_value) == id(var2_value)


def chain_assign(original: list) -> dict:
    a = original
    b = a
    c = b
    return {"a": id(a), "b": id(b), "c": id(c), "original": id(original)}
