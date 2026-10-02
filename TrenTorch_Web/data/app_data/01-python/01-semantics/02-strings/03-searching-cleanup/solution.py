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


def find_all(s: str, sub: str):
    if sub == "":
        return []
    result = []
    start = 0
    while True:
        idx = s.find(sub, start)
        if idx == -1:
            break
        result.append(idx)
        start = idx + 1
    return result


def count_overlapping(s: str, sub: str) -> int:
    return len(find_all(s, sub))


def has_extension(filename: str, ext: str) -> bool:
    return filename.lower().endswith("." + ext.lower())


def classify_token(token: str) -> str:
    if token.isdigit():
        return "digits"
    if token.isalpha():
        return "letters"
    if token.isalnum():
        return "alnum"
    if token.isspace():
        return "space"
    return "other"


def clean_field(s: str) -> str:
    s = s.strip()
    s = s.rstrip(".,;")
    s = s.strip()
    return s


def remove_prefix_once(s: str, prefix: str) -> str:
    if prefix and s.startswith(prefix):
        return s[len(prefix) :]
    return s


def replace_first_n(s: str, old: str, new: str, n: int) -> str:
    if n == 0:
        return s
    if n < 0:
        return s.replace(old, new)
    return s.replace(old, new, n)
