"""
pytest tests.py
"""

import numpy as np

from _load import load_solution

_module = load_solution(__file__)
variance_threshold = _module.variance_threshold
drop_correlated = _module.drop_correlated
select_k_best = _module.select_k_best


# ---- 1-5: variance filter ----


def test_1_constant_column_is_dropped():
    x = np.array([[1.0, 5.0], [2.0, 5.0], [3.0, 5.0]])
    np.testing.assert_array_equal(variance_threshold(x), [True, False])


def test_2_threshold_is_strict():
    x = np.array([[0.0], [2.0]])  # population variance exactly 1
    assert not variance_threshold(x, 1.0)[0]
    assert variance_threshold(x, 0.99)[0]


def test_3_uses_population_variance_not_sample_variance():
    x = np.array([[0.0], [1.0]])  # population 0.25, sample 0.5
    assert not variance_threshold(x, 0.3)[0]


def test_4_returns_a_boolean_array_with_one_entry_per_column():
    result = variance_threshold(np.random.default_rng(0).normal(size=(10, 4)), 0.0)
    assert result.shape == (4,) and result.dtype == bool


def test_5_higher_threshold_keeps_fewer_columns():
    x = np.random.default_rng(1).normal(size=(200, 5)) * np.array([0.1, 0.5, 1.0, 2.0, 4.0])
    assert variance_threshold(x, 0.5).sum() < variance_threshold(x, 0.01).sum()


# ---- 6-11: redundancy filter ----


def test_6_duplicate_column_is_dropped_keeping_the_earlier_one():
    rng = np.random.default_rng(2)
    a = rng.normal(size=100)
    x = np.column_stack([a, rng.normal(size=100), a * 3.0 + 1.0])
    assert drop_correlated(x, 0.95) == [0, 1]


def test_7_negatively_correlated_columns_count_as_redundant():
    a = np.random.default_rng(3).normal(size=100)
    x = np.column_stack([a, -2.0 * a])
    assert drop_correlated(x, 0.9) == [0]


def test_8_independent_columns_are_all_kept():
    x = np.random.default_rng(4).normal(size=(5000, 4))
    assert drop_correlated(x, 0.5) == [0, 1, 2, 3]


def test_9_dropped_columns_are_not_used_to_drop_later_ones():
    # column 2 is correlated with column 1 only; column 1 is dropped (same as
    # column 0), so column 2 is compared against column 0 alone and survives
    # when it is uncorrelated with column 0
    rng = np.random.default_rng(5)
    a = rng.normal(size=4000)
    b = a + 0.01 * rng.normal(size=4000)
    c = 0.8 * b + 0.6 * rng.normal(size=4000)
    kept = drop_correlated(np.column_stack([a, b, c]), 0.9)
    assert kept == [0, 2]


def test_10_constant_column_is_never_dropped_by_correlation():
    a = np.random.default_rng(6).normal(size=50)
    assert drop_correlated(np.column_stack([a, np.ones(50)]), 0.1) == [0, 1]


def test_11_threshold_boundary_is_strict():
    a = np.array([1.0, 2.0, 3.0, 4.0])
    x = np.column_stack([a, a])
    assert drop_correlated(x, 1.0) == [0, 1]  # |r| == 1.0 is not > 1.0
    assert drop_correlated(x, 0.999) == [0]


# ---- 12-17: relevance filter ----


def test_12_picks_the_column_most_related_to_the_label():
    rng = np.random.default_rng(7)
    signal = rng.normal(size=500)
    x = np.column_stack([rng.normal(size=500), signal, rng.normal(size=500)])
    y = 3.0 * signal + 0.1 * rng.normal(size=500)
    np.testing.assert_array_equal(select_k_best(x, y, 1), [1])


def test_13_results_are_ordered_strongest_first():
    rng = np.random.default_rng(8)
    s = rng.normal(size=1000)
    x = np.column_stack([rng.normal(size=1000), s + 2.0 * rng.normal(size=1000), s + 0.1 * rng.normal(size=1000)])
    np.testing.assert_array_equal(select_k_best(x, s, 3)[:2], [2, 1])


def test_14_negative_relationships_score_by_magnitude():
    y = np.array([1.0, 2.0, 3.0, 4.0, 5.0])
    x = np.column_stack([np.array([5.0, 4.0, 3.0, 2.0, 1.0]), np.array([1.0, 0.0, 2.0, 0.0, 1.0])])
    np.testing.assert_array_equal(select_k_best(x, y, 1), [0])


def test_15_ties_go_to_the_lower_index():
    y = np.array([1.0, 2.0, 3.0, 4.0])
    x = np.column_stack([y, y, y])
    np.testing.assert_array_equal(select_k_best(x, y, 2), [0, 1])


def test_16_constant_column_scores_zero():
    y = np.array([1.0, 2.0, 3.0, 4.0])
    x = np.column_stack([np.ones(4), y])
    np.testing.assert_array_equal(select_k_best(x, y, 2), [1, 0])


def test_17_matches_numpy_corrcoef_ranking():
    rng = np.random.default_rng(9)
    x = rng.normal(size=(300, 6))
    y = x @ np.array([0.0, 2.0, -1.0, 0.5, 0.0, 3.0]) + rng.normal(size=300)
    expected = np.argsort(-np.abs([np.corrcoef(x[:, j], y)[0, 1] for j in range(6)]), kind="stable")
    np.testing.assert_array_equal(select_k_best(x, y, 6), expected)


def test_18_inputs_are_not_modified():
    x = np.random.default_rng(10).normal(size=(20, 3))
    y = np.random.default_rng(11).normal(size=20)
    x0, y0 = x.copy(), y.copy()
    variance_threshold(x)
    drop_correlated(x, 0.5)
    select_k_best(x, y, 2)
    np.testing.assert_array_equal(x, x0)
    np.testing.assert_array_equal(y, y0)
