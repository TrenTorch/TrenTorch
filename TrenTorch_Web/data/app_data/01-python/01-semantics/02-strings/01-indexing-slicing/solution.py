def first_and_last(s: str) -> str:
    if len(s) == 0:
        return ""
    if len(s) == 1:
        return s[0] * 2
    return s[0] + s[-1]


def reverse_string(s: str) -> str:
    return s[::-1]


def every_kth_from(s: str, start: int, k: int) -> str:
    return s[start::k]
