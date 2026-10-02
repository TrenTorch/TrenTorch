def utf8_byte_length(s: str) -> int:
    return len(s.encode("utf-8"))


def roundtrip(s: str, encoding: str) -> str:
    encoded = s.encode(encoding, errors="replace")
    return encoded.decode(encoding)


def is_ascii_only(s: str) -> bool:
    return len(s) == len(s.encode("utf-8"))


def first_byte_values(s: str, count: int):
    return list(s.encode("utf-8"))[:count]
