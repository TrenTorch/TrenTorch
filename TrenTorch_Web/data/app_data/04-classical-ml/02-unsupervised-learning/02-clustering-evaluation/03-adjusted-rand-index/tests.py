"""
pytest tests.py
"""

import numpy as np

from _load import load_solution

adjusted_rand_index = load_solution(__file__).adjusted_rand_index


def _raises_value_error(function, *args):
    try:
        function(*args)
    except ValueError:
        return True
    return False


def test_identical_partitions_give_one():
    labels = np.array([0, 0, 1, 1, 2])
    assert np.isclose(adjusted_rand_index(labels, labels), 1.0)


def test_relabeling_does_not_change_the_score():
    a = np.array([0, 0, 1, 1, 2, 2])
    b = np.array([5, 5, 3, 3, 9, 9])
    assert np.isclose(adjusted_rand_index(a, b), 1.0)


def test_orthogonal_partitions_give_minus_one_half():
    # contingency is all ones: expected = 2/3, max = 2, ARI = (0 - 2/3) / (2 - 2/3) = -0.5
    a = np.array([0, 0, 1, 1])
    b = np.array([0, 1, 0, 1])
    assert np.isclose(adjusted_rand_index(a, b), -0.5)


def test_symmetric_in_its_arguments():
    rng = np.random.default_rng(16)
    a = rng.integers(0, 3, size=40)
    b = rng.integers(0, 4, size=40)
    assert np.isclose(adjusted_rand_index(a, b), adjusted_rand_index(b, a))


def test_random_partitions_score_near_zero_on_average():
    rng = np.random.default_rng(17)
    scores = [
        adjusted_rand_index(rng.integers(0, 3, size=300), rng.integers(0, 3, size=300))
        for _ in range(20)
    ]
    assert abs(np.mean(scores)) < 0.02


def test_upper_bound_is_one():
    rng = np.random.default_rng(18)
    for _ in range(5):
        a = rng.integers(0, 4, size=30)
        b = rng.integers(0, 4, size=30)
        assert adjusted_rand_index(a, b) <= 1.0 + 1e-12


def test_merging_two_clusters_lowers_the_score_below_one():
    truth = np.array([0, 0, 1, 1, 2, 2])
    merged = np.array([0, 0, 0, 0, 1, 1])
    assert adjusted_rand_index(truth, merged) < 1.0


def test_one_cluster_against_one_cluster_is_one():
    assert np.isclose(adjusted_rand_index(np.zeros(5, dtype=int), np.zeros(5, dtype=int)), 1.0)


def test_one_cluster_against_many_is_zero():
    assert np.isclose(adjusted_rand_index(np.zeros(4, dtype=int), np.array([0, 1, 2, 3])), 0.0)


def test_string_labels_work():
    a = np.array(["x", "x", "y", "y"])
    b = np.array([1, 1, 2, 2])
    assert np.isclose(adjusted_rand_index(a, b), 1.0)


def test_length_mismatch_raises():
    assert _raises_value_error(adjusted_rand_index, np.array([0, 1]), np.array([0]))


def test_does_not_modify_inputs():
    a = np.array([0, 0, 1])
    b = np.array([0, 1, 1])
    before_a, before_b = a.copy(), b.copy()
    adjusted_rand_index(a, b)
    assert np.array_equal(a, before_a)
    assert np.array_equal(b, before_b)
