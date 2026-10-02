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
