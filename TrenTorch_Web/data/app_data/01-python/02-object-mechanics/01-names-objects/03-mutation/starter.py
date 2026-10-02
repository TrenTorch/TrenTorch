def mutate_list(lst: list) -> None:
    """
    Mutate `lst` in place by appending the value 4 to it.
    Do not reassign lst to a new object. Return nothing.
    """
    pass


def reassign_list(lst: list) -> list:
    """
    Create a brand-new list [9, 9, 9] and return it, without
    mutating the original `lst` in any way.
    """
    pass


def observe_through_alias(original: list) -> dict:
    """
    Inside this function:
      1. Create `alias = original` (a second variable pointing
         at the same object).
      2. Mutate `original` by appending 100 to it.
      3. Reassign `original` to a brand-new list [0, 0, 0]
         (do not mutate this new list into alias's object).

    Return a dictionary:
      {
        "alias_after_mutation": <contents of alias right after step 2>,
        "alias_after_reassignment": <contents of alias right after step 3>,
        "original_final": <contents of original at the end>
      }
    """
    pass


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
