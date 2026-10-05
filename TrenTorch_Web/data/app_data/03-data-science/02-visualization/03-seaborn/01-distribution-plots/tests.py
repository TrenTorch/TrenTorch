"""
pytest tests.py
"""

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import pytest

from _load import load_solution

_module = load_solution(__file__)
histogram_axes = _module.histogram_axes
kde_axes = _module.kde_axes
kde_by_group = _module.kde_by_group
ecdf_axes = _module.ecdf_axes


def _fresh():
    plt.close("all")


def _area(line):
    x, y = np.asarray(line.get_xdata(), float), np.asarray(line.get_ydata(), float)
    return float(np.sum((y[1:] + y[:-1]) / 2 * np.diff(x)))


def _frame(n=240, seed=0):
    rng = np.random.default_rng(seed)
    groups = np.tile(["a", "b", "c"], n // 3)
    x = rng.normal(0, 1, n)
    x[groups == "b"] += 4.0
    return pd.DataFrame({"x": x, "g": groups})


# ---- 1-6: histogram_axes ----


def test_1_one_bar_per_bin():
    _fresh()
    ax = histogram_axes(_frame(), "x", 9, "count")
    assert len(ax.patches) == 9


def test_2_count_bars_match_numpy():
    _fresh()
    df = _frame()
    ax = histogram_axes(df, "x", 7, "count")
    ref, _ = np.histogram(df["x"], bins=7)
    assert [p.get_height() for p in ax.patches] == ref.tolist()


def test_3_bars_sit_on_numpys_bin_edges():
    _fresh()
    df = _frame()
    ax = histogram_axes(df, "x", 6, "count")
    edges = np.histogram_bin_edges(df["x"], bins=6)
    assert [p.get_x() for p in ax.patches] == pytest.approx(edges[:-1].tolist())


def test_4_density_bars_have_total_area_one():
    _fresh()
    ax = histogram_axes(_frame(), "x", 10, "density")
    assert sum(p.get_height() * p.get_width() for p in ax.patches) == pytest.approx(1.0)


def test_5_probability_bars_sum_to_one():
    _fresh()
    ax = histogram_axes(_frame(), "x", 10, "probability")
    assert sum(p.get_height() for p in ax.patches) == pytest.approx(1.0)


def test_6_axis_labels_follow_the_statistic():
    _fresh()
    df = _frame()
    assert histogram_axes(df, "x", 5, "count").get_ylabel() == "Count"
    _fresh()
    assert histogram_axes(df, "x", 5, "density").get_ylabel() == "Density"
    _fresh()
    ax = histogram_axes(df, "x", 5, "probability")
    assert ax.get_ylabel() == "Probability" and ax.get_xlabel() == "x"


# ---- 7-10: kde_axes ----


def test_7_exactly_one_curve():
    _fresh()
    ax = kde_axes(_frame(), "x")
    assert len(ax.lines) == 1


def test_8_the_curve_integrates_to_one():
    _fresh()
    ax = kde_axes(_frame(), "x")
    assert _area(ax.lines[0]) == pytest.approx(1.0, abs=0.01)


def test_9_the_peak_is_near_the_mode_of_the_data():
    _fresh()
    x = np.random.default_rng(1).normal(5.0, 0.5, 500)
    ax = kde_axes(pd.DataFrame({"v": x}), "v")
    line = ax.lines[0]
    peak = line.get_xdata()[int(np.argmax(line.get_ydata()))]
    assert abs(peak - 5.0) < 0.3
    assert ax.get_ylabel() == "Density" and ax.get_xlabel() == "v"


def test_10_a_bimodal_sample_has_two_local_maxima():
    _fresh()
    rng = np.random.default_rng(2)
    x = np.concatenate([rng.normal(-3, 0.5, 300), rng.normal(3, 0.5, 300)])
    ax = kde_axes(pd.DataFrame({"v": x}), "v")
    y = np.asarray(ax.lines[0].get_ydata())
    peaks = int(((y[1:-1] > y[:-2]) & (y[1:-1] > y[2:])).sum())
    assert peaks == 2


# ---- 11-14: kde_by_group ----


def test_11_one_curve_per_group_each_integrating_to_one():
    _fresh()
    ax = kde_by_group(_frame(), "x", "g", ["a", "b", "c"])
    assert len(ax.lines) == 3
    assert all(_area(line) == pytest.approx(1.0, abs=0.02) for line in ax.lines)


def test_12_legend_follows_the_requested_order_and_is_titled_by_the_group():
    _fresh()
    ax = kde_by_group(_frame(), "x", "g", ["c", "a", "b"])
    legend = ax.get_legend()
    assert [t.get_text() for t in legend.get_texts()] == ["c", "a", "b"]
    assert legend.get_title().get_text() == "g"


def test_13_groups_of_different_sizes_still_have_equal_areas():
    _fresh()
    rng = np.random.default_rng(3)
    df = pd.DataFrame({"v": np.concatenate([rng.normal(0, 1, 400), rng.normal(5, 1, 40)]), "k": ["big"] * 400 + ["small"] * 40})
    ax = kde_by_group(df, "v", "k", ["big", "small"])
    areas = sorted(_area(line) for line in ax.lines)
    assert areas[0] == pytest.approx(areas[1], abs=0.02)


def test_14_the_shifted_group_peaks_further_right():
    _fresh()
    ax = kde_by_group(_frame(), "x", "g", ["a", "b", "c"])
    peaks = sorted(float(l.get_xdata()[int(np.argmax(l.get_ydata()))]) for l in ax.lines)
    assert peaks[-1] > 2.5 and peaks[0] < 1.5 and peaks[1] < 1.5


# ---- 15-17: ecdf_axes ----


def test_15_the_curve_ends_at_one_and_starts_at_zero():
    _fresh()
    ax = ecdf_axes(_frame(), "x")
    y = np.asarray(ax.lines[0].get_ydata(), float)
    assert y[0] == 0.0 and y[-1] == 1.0


def test_16_the_steps_sit_at_the_sorted_data_values():
    _fresh()
    df = _frame(n=60)
    ax = ecdf_axes(df, "x")
    x = np.asarray(ax.lines[0].get_xdata(), float)
    assert x[1:].tolist() == pytest.approx(np.sort(df["x"].to_numpy()).tolist())


def test_17_the_height_at_a_value_is_the_fraction_at_or_below_it():
    _fresh()
    df = pd.DataFrame({"v": [1.0, 2.0, 2.0, 3.0, 10.0]})
    ax = ecdf_axes(df, "v")
    x, y = np.asarray(ax.lines[0].get_xdata(), float), np.asarray(ax.lines[0].get_ydata(), float)
    at_three = y[np.flatnonzero(x == 3.0)[-1]]
    assert at_three == pytest.approx(4 / 5)
    assert ax.get_ylabel() == "Proportion"
