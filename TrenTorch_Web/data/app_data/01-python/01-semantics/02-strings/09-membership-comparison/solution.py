def compare_strings(a: str, b: str) -> int:
    for i in range(min(len(a), len(b))):
        if ord(a[i]) < ord(b[i]):
            return -1
        if ord(a[i]) > ord(b[i]):
            return 1
    if len(a) < len(b):
        return -1
    if len(a) > len(b):
        return 1
    return 0


def compare_ignoring_case(a: str, b: str) -> int:
    ca, cb = a.casefold(), b.casefold()
    if ca < cb:
        return -1
    if ca > cb:
        return 1
    return 0


def caesar_shift(s: str, k: int) -> str:
    result = []
    for ch in s:
        if "a" <= ch <= "z":
            base = ord("a")
            result.append(chr((ord(ch) - base + k) % 26 + base))
        elif "A" <= ch <= "Z":
            base = ord("A")
            result.append(chr((ord(ch) - base + k) % 26 + base))
        else:
            result.append(ch)
    return "".join(result)
