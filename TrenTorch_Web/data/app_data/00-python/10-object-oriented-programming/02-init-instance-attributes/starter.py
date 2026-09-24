class Rectangle:
    """
    A rectangle with a width and a height.

    __init__(self, width, height):
        Store the two arguments as instance attributes `width`
        and `height`.
    """

    def __init__(self, width, height):
        pass


class Account:
    """
    A simple account record.

    __init__(self, owner, balance=0, history=None):
        Store `owner` and `balance` as attributes.
        Store `history` as an attribute holding a list of past
        transaction amounts. If `history` is None, use a NEW
        empty list for THIS instance. If a list is given, store
        an independent copy of it (list(history)), so the
        instance does not share the caller's list.
    """

    def __init__(self, owner, balance=0, history=None):
        pass


def make_rectangle(width, height):
    """
    Return a new Rectangle with the given width and height.
    """
    pass


def attributes_of(obj) -> dict:
    """
    Return a NEW dictionary that is a copy of obj.__dict__.
    """
    pass
