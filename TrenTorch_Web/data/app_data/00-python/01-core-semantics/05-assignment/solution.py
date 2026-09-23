def chain_assign(original: list) -> dict:
    a = original
    b = a
    c = b
    return {"a": id(a), "b": id(b), "c": id(c), "original": id(original)}
