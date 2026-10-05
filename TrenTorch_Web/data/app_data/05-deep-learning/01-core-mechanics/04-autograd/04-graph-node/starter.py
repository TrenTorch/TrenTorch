class Value:
    """
    A single node in a computation graph: a scalar `data` value, its
    accumulated `grad`, a set of `_prev` parent nodes (what it was
    built from), and a `_backward` closure that knows how to push
    gradient INTO those parents once this node's own `.grad` is known.

    This is the exact object Backward for addition and Backward for
    multiplication's formulas get wired into: every operator overload
    below builds a new Value AND attaches a _backward closure that
    calls those formulas and ACCUMULATES (+=, never =) into each
    parent's .grad, accumulation matters because the same Value can be
    used in more than one place (see the docstrings below).
    """

    def __init__(self, data: float, _children: tuple = ()):
        self.data = data
        self.grad = 0.0
        self._prev = set(_children)
        self._backward = lambda: None  # leaf nodes do nothing on backward

    def __add__(self, other: "Value | float") -> "Value":
        """
        Wraps `other` in a Value if it's a plain number, builds the
        result Value with both operands as `_prev`, and attaches a
        _backward closure implementing Backward for addition's rule
        (accumulated with +=, into both self.grad and other.grad).
        """
        pass

    def __mul__(self, other: "Value | float") -> "Value":
        """
        Same shape as __add__, but implementing Backward for
        multiplication's rule instead (each parent's gradient scaled
        by the OTHER parent's data value).
        """
        pass
