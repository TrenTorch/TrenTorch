"""
pytest tests.py
"""

import numpy as np

from _load import load_solution

calinski_harabasz_index = load_solution(__file__).calinski_harabasz_index


def _raises_value_error(function, *args):
    try:
        function(*args)
    except ValueError:
        return True
    return False


# centroids (0, 1) and (10, 1); overall mean (5, 1)
# B = 2 * 25 + 2 * 25 = 100, W = 4 * 1 = 4, so CH = (100 / 1) / (4 / 2) = 50
X_TWO = np.array([[0.0, 0.0], [0.0, 2.0], [10.0, 0.0], [10.0, 2.0]])
LABELS_TWO = np.array([0, 0, 1, 1])


def test_worked_example_gives_fifty():
    assert np.isclose(calinski_harabasz_index(X_TWO, LABELS_TWO), 50.0)


def test_better_separation_scores_higher():
    far = X_TWO.copy()
    far[2:] += 10.0
    assert calinski_harabasz_index(far, LABELS_TWO) != calinski_harabasz_index(X_TWO, LABELS_TWO)
    spread_apart = np.array([[0.0, 0.0], [0.0, 2.0], [20.0, 0.0], [20.0, 2.0]])
    assert calinski_harabasz_index(spread_apart, LABELS_TWO) > calinski_harabasz_index(X_TWO, LABELS_TWO)


def test_tighter_clusters_score_higher():
    tight = np.array([[0.0, 0.0], [0.0, 0.2], [10.0, 0.0], [10.0, 0.2]])
    assert calinski_harabasz_index(tight, LABELS_TWO) > calinski_harabasz_index(X_TWO, LABELS_TWO)


def test_zero_within_scatter_returns_infinity():
    X = np.array([[0.0, 0.0], [0.0, 0.0], [10.0, 0.0], [10.0, 0.0]])
    assert calinski_harabasz_index(X, LABELS_TWO) == float("inf")


def test_translation_invariant():
    assert np.isclose(calinski_harabasz_index(X_TWO, LABELS_TWO), calinski_harabasz_index(X_TWO + 7.0, LABELS_TWO))


def test_scaling_all_coordinates_does_not_change_the_ratio():
    # B and W both scale by s squared, so the ratio is unchanged
    assert np.isclose(calinski_harabasz_index(X_TWO, LABELS_TWO), calinski_harabasz_index(4.0 * X_TWO, LABELS_TWO))


def test_label_renaming_does_not_change_the_index():
    assert np.isclose(calinski_harabasz_index(X_TWO, LABELS_TWO), calinski_harabasz_index(X_TWO, np.array([9, 9, 4, 4])))


def test_fewer_than_two_clusters_raises():
    assert _raises_value_error(calinski_harabasz_index, X_TWO, np.array([0, 0, 0, 0]))


def test_as_many_clusters_as_samples_raises():
    assert _raises_value_error(calinski_harabasz_index, X_TWO, np.array([0, 1, 2, 3]))


def test_result_is_positive_for_clear_clusters():
    rng = np.random.default_rng(3)
    X = np.vstack([rng.normal(0, 0.1, (15, 2)), rng.normal(5, 0.1, (15, 2))])
    labels = np.array([0] * 15 + [1] * 15)
    assert calinski_harabasz_index(X, labels) > 0.0


def test_returns_a_python_float():
    assert isinstance(calinski_harabasz_index(X_TWO, LABELS_TWO), float)


def test_does_not_modify_inputs():
    X = X_TWO.copy()
    labels = LABELS_TWO.copy()
    calinski_harabasz_index(X, labels)
    assert np.array_equal(X, X_TWO)
    assert np.array_equal(labels, LABELS_TWO)
