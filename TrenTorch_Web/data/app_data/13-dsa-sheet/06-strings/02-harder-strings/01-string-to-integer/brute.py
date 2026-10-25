import re


def my_atoi(s):
    match = re.match(r"^ *([+-]?)([0-9]+)", s)
    if not match:
        return 0
    value = int(match.group(2)[:20])
    if len(match.group(2)) > 20:
        value = 10**30
    if match.group(1) == "-":
        value = -value
    return max(-(2**31), min(2**31 - 1, value))
