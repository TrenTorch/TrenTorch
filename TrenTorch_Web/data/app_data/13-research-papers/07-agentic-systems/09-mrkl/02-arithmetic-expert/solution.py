import re


def arithmetic_expert(expr):
    m = re.match(r"^\s*(-?\d+(?:\.\d+)?)\s*([+\-*])\s*(-?\d+(?:\.\d+)?)\s*$", expr)
    if not m:
        return None
    a, op, b = float(m.group(1)), m.group(2), float(m.group(3))
    if op == "+":
        return a + b
    if op == "-":
        return a - b
    return a * b
