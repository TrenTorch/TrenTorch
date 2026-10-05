import numpy as np


def class_weights(y: np.ndarray) -> dict:
    """
    Returns a dict {label: n_samples / (n_classes * count_of_label)}.
    """
    # TODO: Count each class and apply the balanced weight formula.
    pass


def random_oversample(X: np.ndarray, y: np.ndarray, rng: np.random.Generator) -> tuple:
    """
    Returns (X_resampled, y_resampled): every original row first, in
    order, then extra rows for each class below the largest class count.
    For each such class in sorted label order, draw
    rng.choice(rows_of_that_class, size=max_count - count, replace=True)
    and append those rows. Every class ends with max_count rows.
    """
    # TODO: Duplicate minority rows until the classes are balanced.
    pass


def random_undersample(X: np.ndarray, y: np.ndarray, rng: np.random.Generator) -> tuple:
    """
    Returns (X_resampled, y_resampled) with every class cut to the
    smallest class count. For each class in sorted label order keep
    rng.choice(rows_of_that_class, size=min_count, replace=False), with
    each class's kept indices sorted. Classes appear in sorted label
    order.
    """
    # TODO: Keep an equal number of rows from every class.
    pass


def interpolate_minority(minority: np.ndarray, n_new: int, rng: np.random.Generator) -> np.ndarray:
    """
    minority: 2D float array (points, features) with at least 2 rows

    Returns an array of shape (n_new, features). For each new point, in
    order: draw two distinct points a, b with
    rng.choice(len(minority), size=2, replace=False), then a weight
    u = rng.random(), and return a + u * (b - a).
    """
    # TODO: Build each synthetic point on the segment between two real ones.
    pass
