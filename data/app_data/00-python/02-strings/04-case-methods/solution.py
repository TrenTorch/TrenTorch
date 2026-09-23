def sentence_case(s: str) -> str:
    if s == "":
        return ""
    return s[0].upper() + s[1:].lower()


def swap_first_char_case(s: str) -> str:
    if s == "":
        return ""
    return s[0].swapcase() + s[1:]


def equal_ignoring_case(a: str, b: str) -> bool:
    return a.casefold() == b.casefold()


def case_kind(s: str) -> str:
    if s.isupper():
        return "upper"
    if s.islower():
        return "lower"
    if s.istitle():
        return "title"
    return "mixed"
