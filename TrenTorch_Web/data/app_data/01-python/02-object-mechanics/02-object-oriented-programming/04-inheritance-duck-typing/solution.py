class Shape:
    def area(self):
        return 0.0

    def describe(self):
        return f"{type(self).__name__} with area {self.area():.2f}"


class Circle(Shape):
    def __init__(self, radius):
        self.radius = radius

    def area(self):
        return 3.14159 * self.radius * self.radius


class Rectangle(Shape):
    def __init__(self, width, height):
        self.width = width
        self.height = height

    def area(self):
        return self.width * self.height


class Square(Rectangle):
    def __init__(self, side):
        super().__init__(side, side)


def total_area(shapes: list) -> float:
    total = 0.0
    for shape in shapes:
        total += shape.area()
    return total


def total_length(containers: list) -> int:
    return sum(len(c) for c in containers)


class Countdown:
    def __init__(self, start):
        self.start = start

    def __len__(self):
        return self.start

    def __getitem__(self, index):
        if 0 <= index < self.start:
            return self.start - index
        raise IndexError(index)


def describe_capabilities(obj) -> list:
    capabilities = []
    if hasattr(obj, "__add__"):
        capabilities.append("add")
    if hasattr(obj, "__call__"):
        capabilities.append("call")
    if hasattr(obj, "__getitem__"):
        capabilities.append("index")
    if hasattr(obj, "__iter__"):
        capabilities.append("iter")
    if hasattr(obj, "__len__"):
        capabilities.append("len")
    return sorted(capabilities)


def first_or_none(obj):
    try:
        return obj[0]
    except (IndexError, KeyError, TypeError):
        return None


def add_all(items: list, start):
    result = start
    for item in items:
        result = result + item
    return result
