class Accumulator:
    """
    Keeps a running total.

    __init__(self):
        Set the attribute `total` to 0.

    add(self, x):
        Add `x` to self.total, then return `self` (so calls can
        be chained).

    value(self):
        Return the current total.
    """

    def __init__(self):
        pass

    def add(self, x):
        pass

    def value(self):
        pass


def add_via_class(acc, x):
    """
    Add `x` to the Accumulator `acc` by calling the method
    THROUGH THE CLASS, not through the instance: use
    Accumulator.add(acc, x). Return the value returned by that
    call.
    """
    pass


def bound_method_target(method):
    """
    `method` is a bound method (for example acc.add). Return the
    instance it is bound to, using the method's __self__
    attribute.
    """
    pass


def chain_adds(acc, numbers: list):
    """
    Add every number in `numbers` to `acc` using method calls
    that return `self`, building one chained expression per
    number (do not store intermediate results). Return `acc`.
    An empty list changes nothing.
    """
    pass
