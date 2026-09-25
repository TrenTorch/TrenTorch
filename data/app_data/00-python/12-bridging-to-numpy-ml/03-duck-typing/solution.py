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
