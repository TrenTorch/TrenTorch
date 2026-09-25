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
