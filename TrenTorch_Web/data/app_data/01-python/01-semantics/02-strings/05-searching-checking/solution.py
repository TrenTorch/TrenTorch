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
