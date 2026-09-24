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
