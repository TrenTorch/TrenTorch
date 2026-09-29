class Tracker:
    count = 0

    def __init__(self, label):
        self.label = label
        Tracker.count = Tracker.count + 1


def where_is_attribute(obj, attr: str) -> str:
    if attr in obj.__dict__:
        return "instance"
    if hasattr(obj, attr):
        return "class"
    return "missing"


def shadow_count(tracker, value: int) -> None:
    tracker.count = value
