from math import factorial


def trailing_zeros(n):
    text = str(factorial(n))
    return len(text) - len(text.rstrip("0"))
