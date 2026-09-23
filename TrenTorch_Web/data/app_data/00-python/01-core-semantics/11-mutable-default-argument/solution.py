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
