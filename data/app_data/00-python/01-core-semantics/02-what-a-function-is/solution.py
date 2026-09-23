def is_even(n: int) -> bool:
    return n % 2 == 0


def greet_formal(name: str, title: str) -> str:
    return f"Good day, {title} {name}."


def apply_twice(func, value):
    return func(func(value))
