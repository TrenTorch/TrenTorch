class Tracker:
    """
    Counts how many Tracker instances have been created.

    Define a CLASS attribute `count`, initialized to 0.

    __init__(self, label):
        Store `label` as an instance attribute, and increase the
        class attribute Tracker.count by 1 (assign through the
        class, not through self).
    """

    def __init__(self, label):
        pass


def where_is_attribute(obj, attr: str) -> str:
    """
    Report where the attribute with the string label `attr` would
    be found for `obj`. Return exactly one of:
      "instance"  if it is in obj's own attributes (obj.__dict__)
      "class"     if it is not in obj's own attributes but is
                  found through the class (hasattr is True)
      "missing"   if the attribute does not exist at all
    """
    pass


def shadow_count(tracker, value: int) -> None:
    """
    Make the given Tracker instance report `value` for `.count`
    WITHOUT changing the shared class attribute Tracker.count:
    assign the attribute through the instance. Return nothing.
    """
    pass
