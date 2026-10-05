"""
pytest tests.py
"""

import numpy as np

from _load import load_solution

_module = load_solution(__file__)
disagreement = _module.disagreement

# N11 = 2, N10 = 2, N01 = 1, N00 = 3 for these two vectors.
A = np.array([1, 1, 1, 1, 0, 0, 0, 0])
B = np.array([1, 1, 0, 0, 1, 0, 0, 0])


def _raises_value_error(function, *args, **kwargs):
    try:
        function(*args, **kwargs)
    except ValueError:
        return True
    return False


def test_hand_example_gives_three_eighths():
    assert np.isclose(disagreement(A, B), 3 / 8)


def test_identical_correctness_patterns_have_zero_disagreement():
    assert disagreement(A, A) == 0.0


def test_complementary_patterns_have_full_disagreement():
    assert disagreement(A, 1 - A) == 1.0


def test_measure_is_symmetric():
    assert disagreement(A, B) == disagreement(B, A)


def test_boolean_inputs_match_integer_inputs():
    assert disagreement(A.astype(bool), B.astype(bool)) == disagreement(A, B)


def test_measure_is_between_zero_and_one():
    rng = np.random.default_rng(0)
    for _ in range(20):
        x = rng.integers(0, 2, size=15)
        y = rng.integers(0, 2, size=15)
        assert 0.0 <= disagreement(x, y) <= 1.0


def test_disagreement_is_at_least_the_gap_in_accuracy():
    # Accuracies are 0.75 and 0.25, a gap of 0.5, and the two vectors disagree on half the examples.
    x = np.array([1, 1, 1, 0])
    y = np.array([0, 0, 1, 0])
    assert disagreement(x, y) >= abs(x.mean() - y.mean()) - 1e-12


def test_reordering_both_vectors_does_not_change_the_result():
    perm = np.array([7, 2, 5, 0, 3, 6, 1, 4])
    assert np.isclose(disagreement(A[perm], B[perm]), disagreement(A, B))


def test_flipping_one_classifier_turns_agreement_into_disagreement():
    assert np.isclose(disagreement(A, 1 - B), 1 - 3 / 8)


def test_all_wrong_versus_all_right_is_full_disagreement():
    assert disagreement(np.ones(5), np.zeros(5)) == 1.0


def test_length_mismatch_raises():
    assert _raises_value_error(disagreement, [1, 0], [1, 0, 1])


def test_empty_input_raises():
    assert _raises_value_error(disagreement, [], [])


def test_two_dimensional_input_raises():
    assert _raises_value_error(disagreement, np.ones((2, 2)), np.ones((2, 2)))


def test_inputs_are_not_modified():
    a = A.copy()
    b = B.copy()
    disagreement(a, b)
    assert np.array_equal(a, A) and np.array_equal(b, B)
