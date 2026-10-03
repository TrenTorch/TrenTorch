import numpy as np


def one_hot_fit(values) -> list:
    return sorted(set(values))


def one_hot_transform(values, categories) -> np.ndarray:
    index = {category: column for column, category in enumerate(categories)}
    out = np.zeros((len(values), len(categories)), dtype=float)
    for row, value in enumerate(values):
        if value not in index:
            raise ValueError(f"unknown category {value!r}")
        out[row, index[value]] = 1.0
    return out
