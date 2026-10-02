def add_item_fixed(item, bucket: list | None = None) -> list:
    """
    Append `item` to `bucket` and return it. If `bucket` is not
    provided (None), create a brand-new empty list inside this
    call — never reuse a list object across separate calls that
    didn't explicitly pass one.
    """
    pass


def is_vulnerable_to_mutable_default(func) -> bool:
    """
    Given a function object `func`, inspect its default argument
    values (available via func.__defaults__) and return True if
    any default value is a mutable object (list, dict, or set),
    False otherwise.
    """
    pass
