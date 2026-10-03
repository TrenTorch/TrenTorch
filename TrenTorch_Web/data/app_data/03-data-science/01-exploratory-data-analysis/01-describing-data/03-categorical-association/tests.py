"""
pytest tests.py
"""

import numpy as np

from _load import load_solution

_module = load_solution(__file__)
contingency_table = _module.contingency_table
expected_counts = _module.expected_counts
chi_square_statistic = _module.chi_square_statistic
cramers_v = _module.cramers_v


# ---- 1-5: contingency table ----


def test_1_table_matches_a_hand_computed_case():
    a = np.array(["x", "x", "y", "y", "y"])
    b = np.array(["p", "q", "p", "p", "q"])
    np.testing.assert_array_equal(contingency_table(a, b), [[1, 1], [2, 1]])


def test_2_rows_and_columns_follow_sorted_label_order():
    a = np.array(["b", "a", "a"])
    b = np.array([2, 1, 2])
    table = contingency_table(a, b)  # rows a, b; columns 1, 2
    np.testing.assert_array_equal(table, [[1, 1], [0, 1]])


def test_3_counts_sum_to_the_number_of_rows():
    rng = np.random.default_rng(0)
    table = contingency_table(rng.integers(0, 4, size=300), rng.integers(0, 3, size=300))
    assert table.sum() == 300 and table.shape == (4, 3)


def test_4_marginals_match_value_counts():
    a = np.array([0, 0, 1, 2, 2, 2])
    b = np.array([1, 0, 1, 0, 1, 1])
    table = contingency_table(a, b)
    np.testing.assert_array_equal(table.sum(axis=1), [2, 1, 3])
    np.testing.assert_array_equal(table.sum(axis=0), [2, 4])


def test_5_returns_an_integer_array():
    assert contingency_table(np.array([0, 1]), np.array([0, 1])).dtype.kind == "i"


# ---- 6-9: expected counts ----


def test_6_expected_counts_hand_computed():
    expected = expected_counts(np.array([[10, 20], [30, 40]]))
    # row totals 30, 70; column totals 40, 60; n = 100
    np.testing.assert_allclose(expected, [[12.0, 18.0], [28.0, 42.0]])


def test_7_expected_counts_keep_the_marginals():
    table = np.array([[3, 1, 6], [2, 8, 5]])
    expected = expected_counts(table)
    np.testing.assert_allclose(expected.sum(axis=1), table.sum(axis=1))
    np.testing.assert_allclose(expected.sum(axis=0), table.sum(axis=0))


def test_8_independent_table_equals_its_expected_counts():
    table = np.array([[10, 20], [30, 60]])  # exact independence
    np.testing.assert_allclose(expected_counts(table), table)


def test_9_expected_counts_are_floats():
    assert expected_counts(np.array([[1, 2], [3, 4]])).dtype.kind == "f"


# ---- 10-14: chi-square ----


def test_10_chi_square_hand_computed():
    # expected [[12, 18], [28, 42]]; sum of (O-E)^2 / E
    table = np.array([[10, 20], [30, 40]])
    expected = np.array([[12.0, 18.0], [28.0, 42.0]])
    want = np.sum((table - expected) ** 2 / expected)
    assert np.isclose(chi_square_statistic(table), want)


def test_11_independent_table_has_zero_statistic():
    assert np.isclose(chi_square_statistic(np.array([[10, 20], [30, 60]])), 0.0)


def test_12_two_by_two_matches_the_shortcut_formula():
    a, b, c, d = 20.0, 5.0, 10.0, 25.0
    n = a + b + c + d
    shortcut = n * (a * d - b * c) ** 2 / ((a + b) * (c + d) * (a + c) * (b + d))
    assert np.isclose(chi_square_statistic(np.array([[a, b], [c, d]])), shortcut)


def test_13_statistic_scales_linearly_with_the_sample_size():
    table = np.array([[10, 20], [30, 15]])
    assert np.isclose(chi_square_statistic(3 * table), 3 * chi_square_statistic(table))


def test_14_empty_row_does_not_cause_a_division_by_zero():
    stat = chi_square_statistic(np.array([[0, 0], [5, 7]]))
    assert np.isfinite(stat)


# ---- 15-19: Cramer's V ----


def test_15_perfect_association_gives_one():
    assert np.isclose(cramers_v(np.array([[50, 0], [0, 50]])), 1.0)
    assert np.isclose(cramers_v(np.array([[30, 0, 0], [0, 20, 0], [0, 0, 10]])), 1.0)


def test_16_independence_gives_zero():
    assert np.isclose(cramers_v(np.array([[10, 20], [30, 60]])), 0.0)


def test_17_value_is_between_zero_and_one_and_unchanged_by_sample_size():
    table = np.array([[20, 10], [5, 25]])
    v = cramers_v(table)
    assert 0.0 < v < 1.0
    assert np.isclose(v, cramers_v(10 * table))


def test_18_degenerate_tables_return_zero():
    assert cramers_v(np.array([[3, 4, 5]])) == 0.0
    assert cramers_v(np.array([[3], [4]])) == 0.0
    assert cramers_v(np.zeros((2, 2))) == 0.0


def test_19_end_to_end_on_related_and_unrelated_columns():
    rng = np.random.default_rng(1)
    device = rng.integers(0, 3, size=4000)
    related = np.where(rng.random(4000) < 0.8, device, rng.integers(0, 3, size=4000))
    unrelated = rng.integers(0, 3, size=4000)
    assert cramers_v(contingency_table(device, related)) > 0.5
    assert cramers_v(contingency_table(device, unrelated)) < 0.1
