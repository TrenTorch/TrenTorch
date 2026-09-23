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
