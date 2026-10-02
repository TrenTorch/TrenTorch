def describe_object(value) -> dict:
    """
    Return a dictionary with two keys:
      - "type": the type of `value`, as a string (e.g. "int", "list").
      - "address": the memory address of `value`, obtained via id().

    Example: describe_object(100) -> {"type": "int", "address": 4385728}
    (the actual address will vary each run)
    """
    pass
