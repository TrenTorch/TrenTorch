def build_instances(cls, count: int) -> list:
    """
    Return a list of `count` NEW instances of the class `cls`,
    each created by calling `cls()` with no arguments. Every
    instance must be a separate object. If count <= 0, return [].
    """
    pass


def attach_point(obj, x: int, y: int) -> None:
    """
    Set two attributes on `obj`: obj.x = x and obj.y = y. If the
    attributes already exist, replace their values. Return
    nothing.
    """
    pass


def same_class(a, b) -> bool:
    """
    Return True if `a` and `b` are instances of exactly the same
    class (compare type(a) and type(b) with `is`).
    """
    pass


def attribute_snapshot(obj) -> dict:
    """
    Return a NEW dictionary containing a copy of the attributes
    stored on `obj` (from obj.__dict__). Changing the returned
    dictionary must not change `obj`.
    """
    pass
