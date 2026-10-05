import math


def dot_loop(a: list, b: list) -> float:
    total = 0.0
    for i in range(len(a)):
        total += a[i] * b[i]
    return total


def loop_time_model(n: int, per_iteration_cost: float) -> float:
    if n <= 0:
        return 0.0
    return n * per_iteration_cost


def vectorized_time_model(n: int, call_overhead: float, per_element_cost: float) -> float:
    if n <= 0:
        return call_overhead
    return call_overhead + n * per_element_cost


def break_even_n(per_iteration_cost: float, call_overhead: float, per_element_cost: float):
    if per_element_cost >= per_iteration_cost:
        return None
    n = call_overhead / (per_iteration_cost - per_element_cost)
    return max(1, math.ceil(n))


def list_of_ints_bytes(n: int) -> int:
    if n <= 0:
        return 0
    return n * 36


def typed_array_bytes(n: int, itemsize: int) -> int:
    if n <= 0:
        return 0
    return n * itemsize
