def build_instances(cls, count: int) -> list:
    if count <= 0:
        return []
    return [cls() for _ in range(count)]


def attach_point(obj, x: int, y: int) -> None:
    obj.x = x
    obj.y = y


def same_class(a, b) -> bool:
    return type(a) is type(b)


def attribute_snapshot(obj) -> dict:
    return dict(obj.__dict__)


class Rectangle:
    def __init__(self, width, height):
        self.width = width
        self.height = height


class Account:
    def __init__(self, owner, balance=0, history=None):
        self.owner = owner
        self.balance = balance
        if history is None:
            history = []
        self.history = list(history)


def make_rectangle(width, height):
    return Rectangle(width, height)


def attributes_of(obj) -> dict:
    return dict(obj.__dict__)
