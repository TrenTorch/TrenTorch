def describe_object(value) -> dict:
    return {"type": type(value).__name__, "address": id(value)}
