import numpy as np


def get_unique_categories(column: np.ndarray) -> np.ndarray:
    return np.unique(column)


def one_hot_encode(column: np.ndarray, categories: np.ndarray | None = None) -> np.ndarray:
    if categories is None:
        categories = get_unique_categories(column)

    category_to_index = {category: i for i, category in enumerate(categories)}
    result = np.zeros((len(column), len(categories)))
    for row, value in enumerate(column):
        result[row, category_to_index[value]] = 1.0
    return result
