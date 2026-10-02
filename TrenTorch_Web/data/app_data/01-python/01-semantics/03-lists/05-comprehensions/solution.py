import math


def squares_of_evens(numbers: list) -> list:
    return [n * n for n in numbers if n % 2 == 0]


def label_parity(numbers: list) -> list:
    return ["even" if n % 2 == 0 else "odd" for n in numbers]


def flatten(nested: list) -> list:
    return [x for row in nested for x in row]


def multiplication_table(n: int) -> list:
    if n <= 0:
        return []
    return [[i * j for j in range(1, n + 1)] for i in range(1, n + 1)]


def elementwise(func, *vectors) -> list:
    return [func(*group) for group in zip(*vectors)]


def mask_select(values: list, mask: list) -> list:
    return [value for value, keep in zip(values, mask) if keep]


def broadcast_add(values: list, other) -> list:
    if hasattr(other, "__len__"):
        return [a + b for a, b in zip(values, other)]
    return [x + other for x in values]


def normalize(values: list, eps: float) -> list:
    n = len(values)
    if n == 0:
        return []
    mean = sum(values) / n
    variance = sum((x - mean) ** 2 for x in values) / n
    denom = math.sqrt(variance + eps)
    return [(x - mean) / denom for x in values]
