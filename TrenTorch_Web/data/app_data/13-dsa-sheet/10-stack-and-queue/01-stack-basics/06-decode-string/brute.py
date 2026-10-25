import re


def decode_string(s):
    pattern = re.compile(r"(\d+)\[([a-z]*)\]")
    while "[" in s:
        s = pattern.sub(lambda m: m.group(2) * int(m.group(1)), s)
    return s
