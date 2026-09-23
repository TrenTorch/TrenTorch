def is_mutable_type(value) -> bool:
    """
    Return True if the type of `value` is mutable (list, dict,
    set, or a typical custom object instance), False if it's
    immutable (int, float, bool, str, tuple, frozenset).
    """
    pass


def tuple_inner_mutation_check(t: tuple) -> dict:
    """
    Given a tuple `t` whose first element is a list, mutate that
    inner list by appending the value 100 to it. Do NOT attempt
    to reassign any slot of the tuple itself.

    Return a dictionary:
      {
        "tuple_id_before": <id of t before mutation>,
        "tuple_id_after": <id of t after mutation>,
        "inner_list_after": <contents of t[0] after mutation>
      }
    tuple_id_before and tuple_id_after should be equal, since the
    tuple itself was never reassigned.
    """
    pass
