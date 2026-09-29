def clean_field(s: str) -> str:
    """
    Return `s` with, in this order:
      1. leading and trailing whitespace removed,
      2. any trailing characters from the set ".,;" removed,
      3. leading and trailing whitespace removed again.

    Example: clean_field("  total ; ")  -> "total"
             clean_field("  a b.. ")    -> "a b"
    """
    pass


def remove_prefix_once(s: str, prefix: str) -> str:
    """
    If `s` begins with `prefix`, return `s` with that prefix
    removed exactly ONCE. Otherwise return `s` unchanged.
    Do not use lstrip(): it removes a set of characters, not a
    prefix.

    Example: remove_prefix_once("ababab", "ab") -> "abab"
    """
    pass


def replace_first_n(s: str, old: str, new: str, n: int) -> str:
    """
    Return `s` with the first `n` occurrences of `old` replaced
    by `new`. If n == 0, return `s` unchanged. If n < 0,
    replace every occurrence.
    """
    pass
