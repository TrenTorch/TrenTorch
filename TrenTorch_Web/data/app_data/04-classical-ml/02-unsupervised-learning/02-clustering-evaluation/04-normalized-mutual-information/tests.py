"""
pytest tests.py
"""

import numpy as np

from _load import load_solution

normalized_mutual_information = load_solution(__file__).normalized_mutual_information


def _raises_value_error(function, *args):
    try:
        function(*args)
    except ValueError:
        return True
    return False


def test_identical_partitions_give_one():
    labels = np.array([0, 0, 1, 1, 2, 2])
    assert np.isclose(normalized_mutual_information(labels, labels), 1.0)


def test_relabeling_does_not_change_the_score():
    a = np.array([0, 0, 1, 1, 2, 2])
    b = np.array([4, 4, 1, 1, 0, 0])
    assert np.isclose(normalized_mutual_information(a, b), 1.0)


def test_independent_partitions_give_zero():
    # every cell of the 2x2 table holds one point, so MI is exactly 0
    a = np.array([0, 0, 1, 1])
    b = np.array([0, 1, 0, 1])
    assert np.isclose(normalized_mutual_information(a, b), 0.0, atol=1e-12)


def test_symmetric_in_its_arguments():
    rng = np.random.default_rng(19)
    a = rng.integers(0, 3, size=50)
    b = rng.integers(0, 4, size=50)
    assert np.isclose(normalized_mutual_information(a, b), normalized_mutual_information(b, a))


def test_result_is_between_zero_and_one():
    rng = np.random.default_rng(20)
    for _ in range(5):
        a = rng.integers(0, 4, size=40)
        b = rng.integers(0, 4, size=40)
        score = normalized_mutual_information(a, b)
        assert 0.0 <= score <= 1.0 + 1e-12


def test_partial_agreement_scores_between_the_extremes():
    truth = np.array([0, 0, 0, 0, 1, 1, 1, 1])
    almost = np.array([0, 0, 0, 1, 1, 1, 1, 1])
    score = normalized_mutual_information(truth, almost)
    assert 0.0 < score < 1.0


def test_better_partition_scores_higher():
    truth = np.array([0, 0, 0, 0, 1, 1, 1, 1])
    good = np.array([0, 0, 0, 0, 1, 1, 1, 0])
    bad = np.array([0, 1, 0, 1, 0, 1, 0, 1])
    assert normalized_mutual_information(truth, good) > normalized_mutual_information(truth, bad)


def test_both_single_cluster_returns_one():
    assert normalized_mutual_information(np.zeros(4, dtype=int), np.zeros(4, dtype=int)) == 1.0


def test_one_side_single_cluster_is_zero():
    truth = np.array([0, 0, 1, 1])
    single = np.zeros(4, dtype=int)
    assert np.isclose(normalized_mutual_information(truth, single), 0.0)


def test_string_labels_work():
    a = np.array(["a", "a", "b", "b"])
    b = np.array([7, 7, 8, 8])
    assert np.isclose(normalized_mutual_information(a, b), 1.0)


def test_length_mismatch_raises():
    assert _raises_value_error(normalized_mutual_information, np.array([0, 1]), np.array([0]))


def test_does_not_modify_inputs():
    a = np.array([0, 1, 1])
    b = np.array([0, 0, 1])
    before_a, before_b = a.copy(), b.copy()
    normalized_mutual_information(a, b)
    assert np.array_equal(a, before_a)
    assert np.array_equal(b, before_b)
