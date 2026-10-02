def replace_char_at(s: str, index: int, ch: str) -> str:
    if index >= len(s) or index < -len(s):
        return s
    if index < 0:
        index += len(s)
    return s[:index] + ch + s[index + 1 :]


def insert_at(s: str, index: int, text: str) -> str:
    return s[:index] + text + s[index:]
