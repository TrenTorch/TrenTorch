"""
pytest tests.py
"""

import numpy as np

from _load import load_solution

_module = load_solution(__file__)
top_k = _module.top_k
competition_ranks = _module.competition_ranks
kth_largest = _module.kth_largest
percentile_rank = _module.percentile_rank

S = np.array([90, 80, 80, 70, 95, 80])


def test_top_k_highest_first():
    np.testing.assert_array_equal(top_k(S, 3), [4, 0, 1])


def test_top_k_ties_go_to_the_lower_index():
    np.testing.assert_array_equal(top_k(S, 5), [4, 0, 1, 2, 5])


def test_top_k_larger_than_the_array_returns_everything():
    assert len(top_k(S, 99)) == len(S)


def test_top_k_k_zero_is_empty():
    assert len(top_k(S, 0)) == 0


def test_competition_ranks_share_the_best_place_and_skip_the_next():
    np.testing.assert_array_equal(competition_ranks(np.array([90, 80, 80, 70])), [1, 2, 2, 4])


def test_competition_ranks_on_a_mixed_example():
    np.testing.assert_array_equal(competition_ranks(S), [2, 3, 3, 6, 1, 3])


def test_competition_ranks_all_equal_and_all_different():
    np.testing.assert_array_equal(competition_ranks(np.array([5, 5, 5])), [1, 1, 1])
    np.testing.assert_array_equal(competition_ranks(np.array([3, 1, 2])), [1, 3, 2])


def test_competition_ranks_match_a_brute_force_count():
    s = np.random.default_rng(0).integers(0, 8, size=40)
    expected = [1 + int((s > x).sum()) for x in s]
    np.testing.assert_array_equal(competition_ranks(s), expected)


def test_kth_largest_values():
    assert kth_largest(S, 1) == 95
    assert kth_largest(S, 2) == 90
    assert kth_largest(S, 3) == 80
    assert kth_largest(S, 6) == 70


def test_kth_largest_matches_a_full_sort():
    s = np.random.default_rng(1).normal(size=51)
    for k in (1, 7, 25, 51):
        assert kth_largest(s, k) == np.sort(s)[::-1][k - 1]


def test_kth_largest_does_not_change_the_input():
    s = S.copy()
    kth_largest(s, 2)
    np.testing.assert_array_equal(s, S)


def test_percentile_rank_is_the_fraction_strictly_smaller():
    np.testing.assert_allclose(percentile_rank(np.array([10, 20, 20, 30])), [0.0, 0.25, 0.25, 0.75])


def test_percentile_rank_matches_a_brute_force_count():
    s = np.random.default_rng(2).integers(0, 10, size=30)
    expected = [(s < x).sum() / len(s) for x in s]
    np.testing.assert_allclose(percentile_rank(s), expected)
