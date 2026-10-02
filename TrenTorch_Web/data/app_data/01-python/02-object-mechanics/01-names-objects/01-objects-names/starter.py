def describe_object(value) -> dict:
    """
    Return a dictionary with two keys:
      - "type": the type of `value`, as a string (e.g. "int", "list").
      - "address": the memory address of `value`, obtained via id().

    Example: describe_object(100) -> {"type": "int", "address": 4385728}
    (the actual address will vary each run)
    """
    pass


def same_object(var1_value, var2_value) -> bool:
    """
    Given two values already assigned to two separate variables
    by the caller, determine whether they point at the same
    object in memory (not just equal values).

    Return True if they store the same address, False otherwise.
    """
    pass


def chain_assign(original: list) -> dict:
    """
    Given a list `original`, perform the following inside this
    function:
      a = original
      b = a
      c = b

    Return a dictionary with keys "a", "b", "c", "original", each
    mapped to the id() of that variable's referenced object.

    All four values in the returned dictionary should be equal,
    since no new object should ever be created by this function.
    """
    pass
