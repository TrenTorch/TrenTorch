def append_in_place(lst: list, value) -> None:
    lst.append(value)


def attempt_reassign(lst: list) -> None:
    lst = [0, 0, 0]


def add_one(x: int) -> int:
    return x + 1


def add_item_fixed(item, bucket: list | None = None) -> list:
    if bucket is None:
        bucket = []
    bucket.append(item)
    return bucket


def is_vulnerable_to_mutable_default(func) -> bool:
    defaults = func.__defaults__
    if not defaults:
        return False
    return any(isinstance(default, (list, dict, set)) for default in defaults)
