def replace_char_at(s: str, index: int, ch: str) -> str:
    """
    Return a new string equal to `s` with the character at
    position `index` replaced by `ch`. `index` may be negative.
    `ch` may be any string, not necessarily one character long.

    If `index` is out of range (index >= len(s) or
    index < -len(s)), return `s` unchanged.
    Do not use the replace() method.

    Example: replace_char_at("hello", 0, "J") -> "Jello"
    """
    pass


def insert_at(s: str, index: int, text: str) -> str:
    """
    Return a new string with `text` inserted before position
    `index`. Slice semantics apply: an `index` at or beyond
    len(s) appends, and a negative `index` counts from the end
    (clamped at the start of the string).

    Examples:
      insert_at("abc", 1, "X")   -> "aXbc"
      insert_at("abc", -1, "X")  -> "abXc"
      insert_at("abc", 99, "X")  -> "abcX"
    """
    pass
