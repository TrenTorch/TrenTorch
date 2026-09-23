def compare_strings(a: str, b: str) -> int:
    """
    Compare `a` and `b` lexicographically by code point, WITHOUT
    using the <, >, or == operators on the whole strings. Use a
    loop over positions with ord() on individual characters.

    Return -1 if a < b, 0 if a == b, 1 if a > b.
    A string that is a proper prefix of another is smaller.
    """
    pass


def compare_ignoring_case(a: str, b: str) -> int:
    """
    Same return convention as compare_strings, but the strings
    are compared after applying casefold() to both. You may use
    the built-in comparison operators here.
    """
    pass


def caesar_shift(s: str, k: int) -> str:
    """
    Shift every ASCII letter in `s` forward by `k` positions in
    the alphabet, wrapping from "z" to "a" (and "Z" to "A").
    Case is preserved. Characters that are not ASCII letters are
    left unchanged. `k` may be negative or larger than 26.
    Use ord(), chr(), and %.

    Example: caesar_shift("Abc, xyz!", 3) -> "Def, abc!"
    """
    pass
