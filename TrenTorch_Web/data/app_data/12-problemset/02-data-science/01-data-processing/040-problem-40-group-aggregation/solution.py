import numpy as np

def solve(keys, values):
    accumulator = {}
    for key, value in zip(keys, values):
        total, count = accumulator.get(key, (0.0, 0))
        accumulator[key] = (total + value, count + 1)
    return {key: total / count for key, (total, count) in accumulator.items()}
