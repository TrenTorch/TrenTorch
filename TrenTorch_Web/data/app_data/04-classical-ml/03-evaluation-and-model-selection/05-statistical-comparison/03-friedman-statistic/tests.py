"""
pytest tests.py
"""

import numpy as np

from _load import load_solution

_module = load_solution(__file__)
friedman_statistic = _module.friedman_statistic


def _raises_value_error(function, *args, **kwargs):
    try:
        function(*args, **kwargs)
    except ValueError:
        return True
    return False


PERFECT_ORDER = np.array([[3.0, 2.0, 1.0], [3.0, 2.0, 1.0], [3.0, 2.0, 1.0]])


def test_perfectly_consistent_ranking_matches_hand_value():
    # Rank sums 3, 6, 9: 12/36 * 126 - 36 = 6.
    assert np.isclose(friedman_statistic(PERFECT_ORDER), 6.0)


def test_all_tied_scores_give_zero():
    assert np.isclose(friedman_statistic(np.ones((4, 3))), 0.0)


def test_statistic_is_invariant_to_monotone_rescaling_of_scores():
    rng = np.random.default_rng(0)
    S = rng.random((5, 4))
    assert np.isclose(friedman_statistic(S), friedman_statistic(np.exp(3 * S)))


def test_column_order_permutation_does_not_change_statistic():
    rng = np.random.default_rng(1)
    S = rng.random((6, 4))
    perm = [2, 0, 3, 1]
    assert np.isclose(friedman_statistic(S), friedman_statistic(S[:, perm]))


def test_row_order_permutation_does_not_change_statistic():
    rng = np.random.default_rng(2)
    S = rng.random((6, 3))
    assert np.isclose(friedman_statistic(S), friedman_statistic(S[::-1]))


def test_more_datasets_with_same_pattern_scale_statistic():
    small = friedman_statistic(PERFECT_ORDER)
    big = friedman_statistic(np.tile(PERFECT_ORDER, (2, 1)))
    assert np.isclose(big, 2 * small)


def test_statistic_is_nonnegative():
    rng = np.random.default_rng(3)
    for _ in range(10):
        assert friedman_statistic(rng.random((5, 4))) >= -1e-9


def test_two_column_perfect_order_hand_value():
    # Column 1 always best: rank sums 3 and 6, so 12/(3*2*3) * (9 + 36) - 3*3*3 = 30 - 27 = 3.
    S = np.array([[2.0, 1.0], [2.0, 1.0], [2.0, 1.0]])
    R = np.array([3.0, 6.0])
    expected = 12.0 / (3 * 2 * 3) * np.sum(R ** 2) - 3 * 3 * 3
    assert np.isclose(friedman_statistic(S), expected)


def test_tied_pair_shares_average_rank():
    # Row ranks are [1.5, 1.5, 3]; rank sums become 4.5, 4.5, 9 over N = 3 rows.
    S = np.array([[5.0, 5.0, 1.0], [5.0, 5.0, 1.0], [5.0, 5.0, 1.0]])
    expected = 12.0 / (3 * 3 * 4) * (4.5 ** 2 + 4.5 ** 2 + 9 ** 2) - 3 * 3 * 4
    assert np.isclose(friedman_statistic(S), expected)


def test_one_dimensional_input_raises():
    assert _raises_value_error(friedman_statistic, np.array([1.0, 2.0, 3.0]))


def test_single_algorithm_raises():
    assert _raises_value_error(friedman_statistic, np.ones((3, 1)))


def test_non_finite_score_raises():
    S = np.array([[1.0, np.nan], [2.0, 1.0]])
    assert _raises_value_error(friedman_statistic, S)


def test_inputs_are_not_modified():
    S = PERFECT_ORDER.copy()
    friedman_statistic(S)
    assert np.array_equal(S, PERFECT_ORDER)
