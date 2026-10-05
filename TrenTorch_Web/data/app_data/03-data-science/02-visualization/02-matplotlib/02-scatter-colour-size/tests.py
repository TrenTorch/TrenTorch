"""
pytest tests.py
"""

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
import pytest
from matplotlib.colors import to_hex

from _load import load_solution

_module = load_solution(__file__)
scatter_chart = _module.scatter_chart
fit_line = _module.fit_line
highlight_outliers = _module.highlight_outliers


def _fresh():
    plt.close("all")


# ---- 1-7: scatter_chart ----


def test_1_one_scatter_collection_with_the_points():
    _fresh()
    _, ax, points = scatter_chart([1, 2, 3], [4, 5, 6], [10, 20, 30], [0.1, 0.5, 0.9], "score")
    assert len(ax.collections) == 1
    assert points is ax.collections[0]
    assert points.get_offsets().tolist() == [[1, 4], [2, 5], [3, 6]]


def test_2_marker_sizes_are_the_given_areas():
    _fresh()
    _, _, points = scatter_chart([1, 2, 3], [1, 2, 3], [10, 40, 90], [1, 2, 3], "v")
    assert points.get_sizes().tolist() == [10, 40, 90]


def test_3_colours_come_from_the_values_with_viridis():
    _fresh()
    _, _, points = scatter_chart([1, 2, 3], [1, 2, 3], [20, 20, 20], [5.0, 6.0, 9.0], "v")
    assert points.get_array().tolist() == [5.0, 6.0, 9.0]
    assert points.get_cmap().name == "viridis"


def test_4_a_colourbar_with_the_label_is_added():
    _fresh()
    fig, ax, _ = scatter_chart([1, 2], [1, 2], [20, 20], [1.0, 2.0], "temperature")
    assert len(fig.axes) == 2
    assert fig.axes[1].get_ylabel() == "temperature"


def test_5_returns_a_figure_with_the_axes_in_it():
    _fresh()
    fig, ax, _ = scatter_chart([1, 2], [1, 2], [20, 20], [1.0, 2.0], "v")
    assert ax in fig.axes


def test_6_accepts_numpy_arrays():
    _fresh()
    x = np.linspace(0, 1, 6)
    _, _, points = scatter_chart(x, x**2, np.full(6, 30.0), x, "v")
    assert np.allclose(points.get_offsets()[:, 1], x**2)


def test_7_colours_are_distinct_for_distinct_values():
    _fresh()
    fig, ax, points = scatter_chart([1, 2], [1, 2], [20, 20], [0.0, 1.0], "v")
    fig.canvas.draw()
    colours = points.get_facecolors()
    assert to_hex(colours[0]) != to_hex(colours[1])


# ---- 8-12: fit_line ----


def test_8_returns_the_least_squares_slope_and_intercept_as_floats():
    _fresh()
    _, ax = plt.subplots()
    slope, intercept = fit_line(ax, [0, 1, 2, 3], [1, 3, 5, 7])
    assert type(slope) is float and type(intercept) is float
    assert slope == pytest.approx(2.0) and intercept == pytest.approx(1.0)


def test_9_matches_numpy_on_noisy_data():
    _fresh()
    rng = np.random.default_rng(0)
    x = rng.uniform(0, 10, 40)
    y = 3 * x - 2 + rng.normal(0, 1, 40)
    _, ax = plt.subplots()
    slope, intercept = fit_line(ax, x, y)
    ref = np.polyfit(x, y, 1)
    assert slope == pytest.approx(ref[0]) and intercept == pytest.approx(ref[1])


def test_10_draws_one_red_segment_from_min_to_max_x():
    _fresh()
    _, ax = plt.subplots()
    fit_line(ax, [4, 1, 3, 2], [8, 2, 6, 4])
    assert len(ax.lines) == 1
    line = ax.lines[0]
    xs = line.get_xdata().tolist()
    assert xs == [1.0, 4.0]
    assert line.get_ydata().tolist() == pytest.approx([2.0, 8.0])
    assert to_hex(line.get_color()) == to_hex("red")


def test_11_the_line_is_labelled_fit():
    _fresh()
    _, ax = plt.subplots()
    fit_line(ax, [0, 1], [0, 1])
    assert ax.lines[0].get_label() == "fit"


def test_12_does_not_remove_existing_artists():
    _fresh()
    fig, ax, points = scatter_chart([0, 1, 2], [0, 1, 2], [20, 20, 20], [1, 2, 3], "v")
    fit_line(ax, [0, 1, 2], [0, 1, 2])
    assert len(ax.collections) == 1 and len(ax.lines) == 1


# ---- 13-17: highlight_outliers ----


def test_13_counts_the_points_beyond_k_standard_deviations():
    _fresh()
    _, ax = plt.subplots()
    x = list(range(10))
    y = [0.0] * 9 + [100.0]
    assert highlight_outliers(ax, x, y, 2.0) == 1


def test_14_draws_a_second_red_scatter_with_just_those_points():
    _fresh()
    _, ax = plt.subplots()
    ax.scatter(range(10), [0.0] * 9 + [100.0])
    highlight_outliers(ax, list(range(10)), [0.0] * 9 + [100.0], 2.0)
    assert len(ax.collections) == 2
    extra = ax.collections[1]
    assert extra.get_offsets().tolist() == [[9, 100.0]]
    assert to_hex(extra.get_facecolors()[0]) == to_hex("red")
    assert extra.get_sizes().tolist() == [80.0]


def test_15_returns_an_int_and_draws_nothing_when_there_are_no_outliers():
    _fresh()
    _, ax = plt.subplots()
    n = highlight_outliers(ax, [1, 2, 3, 4], [1.0, 2.0, 3.0, 4.0], 3.0)
    assert n == 0 and type(n) is int
    assert len(ax.collections) == 0


def test_16_the_threshold_is_strict():
    _fresh()
    _, ax = plt.subplots()
    y = np.array([0.0, 0.0, 0.0, 0.0])
    # std = 0, mean = 0, every |y - mean| is 0, not greater than 0
    assert highlight_outliers(ax, [1, 2, 3, 4], y, 0.0) == 0


def test_17_matches_a_numpy_reference():
    _fresh()
    rng = np.random.default_rng(3)
    x = np.arange(60.0)
    y = rng.normal(0, 1, 60)
    y[[5, 40]] = [9.0, -8.0]
    _, ax = plt.subplots()
    expected = int((np.abs(y - y.mean()) > 2.5 * y.std()).sum())
    assert highlight_outliers(ax, x, y, 2.5) == expected
