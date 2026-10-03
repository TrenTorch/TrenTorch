"""
pytest tests.py
"""

import numpy as np

from _load import load_solution

_module = load_solution(__file__)
five_number_summary = _module.five_number_summary
box_plot_stats = _module.box_plot_stats


# ---- 1-5: five-number summary ----


def test_1_hand_computed_summary():
    assert five_number_summary(np.array([1.0, 2.0, 3.0, 4.0, 5.0])) == (1.0, 2.0, 3.0, 4.0, 5.0)


def test_2_interpolates_between_order_statistics():
    summary = five_number_summary(np.array([1.0, 2.0, 3.0, 4.0]))
    assert summary == (1.0, 1.75, 2.5, 3.25, 4.0)


def test_3_unsorted_input_gives_the_same_answer():
    x = np.random.default_rng(0).normal(size=51)
    assert five_number_summary(x) == five_number_summary(np.sort(x))


def test_4_matches_numpy():
    x = np.random.default_rng(1).exponential(size=200)
    expected = (x.min(), *np.percentile(x, [25, 50, 75]), x.max())
    np.testing.assert_allclose(five_number_summary(x), expected)


def test_5_single_value_repeats_everywhere():
    assert five_number_summary(np.array([7.0])) == (7.0, 7.0, 7.0, 7.0, 7.0)


# ---- 6-14: box plot statistics ----


def test_6_no_outliers_whiskers_reach_the_extremes():
    stats = box_plot_stats(np.arange(1.0, 11.0))
    assert stats["lower_whisker"] == 1.0 and stats["upper_whisker"] == 10.0
    assert len(stats["outliers"]) == 0


def test_7_high_outlier_is_flagged_and_the_whisker_stops_short():
    x = np.array([1.0, 2.0, 3.0, 4.0, 5.0, 100.0])
    stats = box_plot_stats(x)
    np.testing.assert_array_equal(stats["outliers"], [100.0])
    assert stats["upper_whisker"] == 5.0


def test_8_low_outliers_are_flagged_too_and_returned_sorted():
    x = np.array([-90.0, -80.0, 10.0, 11.0, 12.0, 13.0, 14.0, 15.0])
    stats = box_plot_stats(x)
    np.testing.assert_array_equal(stats["outliers"], [-90.0, -80.0])
    assert stats["lower_whisker"] == 10.0


def test_9_quartiles_are_reported_in_the_dict():
    x = np.arange(1.0, 10.0)
    stats = box_plot_stats(x)
    assert (stats["q1"], stats["median"], stats["q3"]) == (3.0, 5.0, 7.0)


def test_10_a_value_exactly_on_the_fence_is_not_an_outlier():
    # q1 = 2, q3 = 4, IQR = 2, upper fence = 4 + 1.5 * 2 = 7
    x = np.array([1.0, 2.0, 3.0, 4.0, 5.0, 7.0])
    stats = box_plot_stats(np.array([0.0, 2.0, 2.0, 4.0, 4.0, 7.0]))
    assert stats["upper_whisker"] == 7.0 and len(stats["outliers"]) == 0
    assert x.size == 6


def test_11_larger_whisker_factor_flags_fewer_outliers():
    x = np.append(np.random.default_rng(2).normal(size=200), [4.5, 5.5])
    assert len(box_plot_stats(x, 3.0)["outliers"]) <= len(box_plot_stats(x, 1.5)["outliers"])


def test_12_zero_whisker_factor_makes_the_box_the_whiskers():
    x = np.arange(1.0, 10.0)
    stats = box_plot_stats(x, 0.0)
    assert stats["lower_whisker"] == 3.0 and stats["upper_whisker"] == 7.0
    assert len(stats["outliers"]) == 4


def test_13_whiskers_are_real_data_values():
    x = np.random.default_rng(3).normal(size=100)
    stats = box_plot_stats(x)
    assert stats["lower_whisker"] in x and stats["upper_whisker"] in x


def test_14_inside_plus_outside_account_for_every_value():
    x = np.random.default_rng(4).standard_t(2, size=300)
    stats = box_plot_stats(x)
    inside = np.sum((x >= stats["lower_whisker"]) & (x <= stats["upper_whisker"]))
    assert inside + len(stats["outliers"]) == 300


def test_15_input_is_not_modified():
    x = np.array([5.0, 1.0, 9.0, 3.0, 100.0])
    original = x.copy()
    box_plot_stats(x)
    five_number_summary(x)
    np.testing.assert_array_equal(x, original)
