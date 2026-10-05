"""
pytest tests.py
"""

import numpy as np

from _load import load_solution

_module = load_solution(__file__)
q_statistic = _module.q_statistic

# N11 = 2, N10 = 2, N01 = 1, N00 = 3 for these two vectors.
A = np.array([1, 1, 1, 1, 0, 0, 0, 0])
B = np.array([1, 1, 0, 0, 1, 0, 0, 0])


def _raises_value_error(function, *args, **kwargs):
    try:
        function(*args, **kwargs)
    except ValueError:
        return True
    return False


def test_hand_example_gives_one_half():
    # (2 * 3 - 2 * 1) / (2 * 3 + 2 * 1) = 4 / 8
    assert np.isclose(q_statistic(A, B), 0.5)


def test_identical_patterns_give_one():
    assert np.isclose(q_statistic(A, A), 1.0)


def test_complementary_patterns_give_minus_one():
    assert np.isclose(q_statistic(A, 1 - A), -1.0)


def test_measure_is_symmetric():
    assert np.isclose(q_statistic(A, B), q_statistic(B, A))


def test_boolean_inputs_match_integer_inputs():
    assert np.isclose(q_statistic(A.astype(bool), B.astype(bool)), q_statistic(A, B))


def test_value_stays_in_minus_one_to_one_on_random_data():
    rng = np.random.default_rng(0)
    checked = 0
    for _ in range(40):
        x = rng.integers(0, 2, size=20)
        y = rng.integers(0, 2, size=20)
        try:
            q = q_statistic(x, y)
        except ValueError:
            continue
        checked += 1
        assert -1.0 - 1e-12 <= q <= 1.0 + 1e-12
    assert checked > 0


def test_permuting_examples_does_not_change_q():
    perm = np.array([7, 2, 5, 0, 3, 6, 1, 4])
    assert np.isclose(q_statistic(A[perm], B[perm]), q_statistic(A, B))


def test_all_right_for_one_classifier_is_undefined():
    # N11 = 0 and N00 = 0, and N10 = 5 with N01 = 0, so the denominator is zero.
    assert _raises_value_error(q_statistic, np.ones(5), np.zeros(5))


def test_flipping_one_classifier_negates_q():
    # Flipping B swaps N11 with N10 and N01 with N00: (2 * 1 - 3 * 2) / (2 * 1 + 3 * 2) = -0.5.
    assert np.isclose(q_statistic(A, 1 - B), -0.5)
    assert np.isclose(q_statistic(A, 1 - B), -q_statistic(A, B))


def test_length_mismatch_raises():
    assert _raises_value_error(q_statistic, [1, 0], [1, 0, 1])


def test_empty_input_raises():
    assert _raises_value_error(q_statistic, [], [])


def test_two_dimensional_input_raises():
    assert _raises_value_error(q_statistic, np.ones((2, 2)), np.ones((2, 2)))


def test_inputs_are_not_modified():
    a = A.copy()
    b = B.copy()
    q_statistic(a, b)
    assert np.array_equal(a, A) and np.array_equal(b, B)
