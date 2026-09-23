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
