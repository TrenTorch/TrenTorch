import numpy as np


def contingency_table(a: np.ndarray, b: np.ndarray) -> np.ndarray:
    a = np.asarray(a)
    b = np.asarray(b)
    _, a_index = np.unique(a, return_inverse=True)
    _, b_index = np.unique(b, return_inverse=True)
    table = np.zeros((a_index.max() + 1, b_index.max() + 1), dtype=int)
    np.add.at(table, (a_index, b_index), 1)
    return table


def expected_counts(table: np.ndarray) -> np.ndarray:
    table = np.asarray(table, dtype=float)
    return np.outer(table.sum(axis=1), table.sum(axis=0)) / table.sum()


def chi_square_statistic(table: np.ndarray) -> float:
    observed = np.asarray(table, dtype=float)
    expected = expected_counts(observed)
    positive = expected > 0
    return float(np.sum((observed[positive] - expected[positive]) ** 2 / expected[positive]))


def cramers_v(table: np.ndarray) -> float:
    table = np.asarray(table, dtype=float)
    n = table.sum()
    rows, columns = table.shape
    smaller = min(rows - 1, columns - 1)
    if smaller == 0 or n == 0:
        return 0.0
    return float(np.sqrt(chi_square_statistic(table) / (n * smaller)))
