def replace_char_at(s: str, index: int, ch: str) -> str:
    if index >= len(s) or index < -len(s):
        return s
    if index < 0:
        index += len(s)
    return s[:index] + ch + s[index + 1 :]


def insert_at(s: str, index: int, text: str) -> str:
    return s[:index] + text + s[index:]


def join_with_separator(parts, sep: str) -> str:
    result = ""
    for index, part in enumerate(parts):
        if index > 0:
            result += sep
        result += part
    return result


def repeat_text(s: str, n: int) -> str:
    if n <= 0:
        return ""
    return s * n


def total_chars_copied(n: int, piece_length: int) -> int:
    if n <= 0:
        return 0
    return piece_length * n * (n + 1) // 2
