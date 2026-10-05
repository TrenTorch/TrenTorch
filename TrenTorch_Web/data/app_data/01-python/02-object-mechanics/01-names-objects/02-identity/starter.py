def did_mutate_in_place(lst: list, operation) -> bool:
    """
    `operation` is a function that takes a list and either
    mutates it in place and returns None (e.g. lambda l:
    l.append(99)), or returns a brand-new list without touching
    the original (e.g. lambda l: l + [99]).

    Record id(lst) before calling operation(lst). Call
    operation(lst). If it returned something other than None,
    that return value is the list to use going forward (reassign
    your local `lst` reference to it). Record id() again on
    whichever list you're now referencing.

    Return True if the id() is unchanged (mutated in place),
    False if it changed (a new list was created).
    """
    pass


def are_same_object(a, b) -> bool:
    """
    Return True if `a` and `b` refer to the exact same object,
    using id(), not ==.
    """
    pass


def classify_pair(a, b) -> str:
    """
    Compare a and b using both == and is.
    Return exactly one of these strings:
      "identical"            - a is b (implies == is also True)
      "equal_not_identical"  - == is True but is is False
      "not_equal"             - == is False (is will also be False)
    """
    pass
