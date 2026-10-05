class Shape:
    """
    Base class.

    area(self):
        Return 0.0 (a generic shape has no area). Subclasses
        override this.

    describe(self):
        Return a string of the form
            "<ClassName> with area <area>"
        where <ClassName> is type(self).__name__ and <area> is
        self.area() formatted with exactly 2 decimals. It must
        call self.area().
        Example: "Circle with area 3.14"
    """

    def area(self):
        pass

    def describe(self):
        pass


class Circle(Shape):
    """
    __init__(self, radius): store `radius`.
    area(self): return 3.14159 * radius * radius.
    """

    def __init__(self, radius):
        pass

    def area(self):
        pass


class Rectangle(Shape):
    """
    __init__(self, width, height): store both.
    area(self): return width * height.
    """

    def __init__(self, width, height):
        pass

    def area(self):
        pass


class Square(Rectangle):
    """
    __init__(self, side): call the parent's __init__ through
    super() with side as both width and height. Do not store
    width and height directly in this class.
    Do not define area() here: inherit it.
    """

    def __init__(self, side):
        pass


def total_area(shapes: list) -> float:
    """
    Return the sum of area() over every shape in `shapes`
    (any mix of the classes above). An empty list gives 0.0.
    """
    pass


def total_length(containers: list) -> int:
    """
    Return the sum of len(c) for every element c of `containers`.
    Do not check the types of the elements. An empty list gives 0.
    """
    pass


class Countdown:
    """
    A read-only sequence that counts down from `start`.

    __init__(self, start): store the int `start` (start >= 0).

    __len__(self): return `start`.

    __getitem__(self, index):
        For 0 <= index < start, return start - index. For any
        other index (negative or too large), raise IndexError.
        (Once this works, list(Countdown(3)) is [3, 2, 1] with
        no __iter__ defined.)
    """

    def __init__(self, start):
        pass

    def __len__(self):
        pass

    def __getitem__(self, index):
        pass


def describe_capabilities(obj) -> list:
    """
    Return a SORTED list of the following labels, one for each
    capability that `obj` has, checked with hasattr():
      "add"    if it has __add__
      "call"   if it has __call__
      "index"  if it has __getitem__
      "iter"   if it has __iter__
      "len"    if it has __len__
    Example: describe_capabilities(5)       -> ["add"]
             describe_capabilities([1, 2])  -> ["add", "index", "iter", "len"]
    """
    pass


def first_or_none(obj):
    """
    Return obj[0]. If that raises an IndexError, KeyError, or
    TypeError, return None. Handle it with try/except (do not
    check the type first).
    """
    pass


def add_all(items: list, start):
    """
    Return `start + items[0] + items[1] + ...`, applying + from
    left to right using a loop, with no type checks. It must work
    for numbers, strings, and lists alike. An empty `items`
    returns `start` unchanged.
    """
    pass
