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
small_multiples = _module.small_multiples
twin_axis_chart = _module.twin_axis_chart
set_limits_and_ticks = _module.set_limits_and_ticks


def _fresh():
    plt.close("all")


def _series(n):
    x = [0, 1, 2]
    return {f"g{i}": (x, [i, i + 1, i + 2]) for i in range(n)}


def _shared_x(a, b):
    return a.get_shared_x_axes().joined(a, b)


def _shared_y(a, b):
    return a.get_shared_y_axes().joined(a, b)


# ---- 1-8: small_multiples ----


def test_1_grid_shape_is_ceil_of_panels_over_columns():
    _fresh()
    _, axes = small_multiples(_series(5), 2)
    assert axes.shape == (3, 2)
    _, axes = small_multiples(_series(4), 2)
    assert axes.shape == (2, 2)


def test_2_a_single_row_is_still_a_2d_array():
    _fresh()
    _, axes = small_multiples(_series(3), 3)
    assert axes.shape == (1, 3)


def test_3_each_panel_has_its_title_in_row_major_order():
    _fresh()
    _, axes = small_multiples(_series(4), 2)
    assert [ax.get_title() for ax in axes.flat] == ["g0", "g1", "g2", "g3"]


def test_4_each_panel_draws_its_own_line():
    _fresh()
    _, axes = small_multiples(_series(4), 2)
    for i, ax in enumerate(axes.flat):
        assert len(ax.lines) == 1
        assert ax.lines[0].get_ydata().tolist() == [i, i + 1, i + 2]


def test_5_all_panels_share_the_x_axis():
    _fresh()
    _, axes = small_multiples(_series(4), 2)
    flat = list(axes.flat)
    assert all(_shared_x(flat[0], other) for other in flat[1:])


def test_6_all_panels_share_the_y_axis():
    _fresh()
    _, axes = small_multiples(_series(4), 2)
    flat = list(axes.flat)
    assert all(_shared_y(flat[0], other) for other in flat[1:])


def test_7_leftover_panels_are_hidden_and_used_ones_are_visible():
    _fresh()
    _, axes = small_multiples(_series(5), 2)
    flat = list(axes.flat)
    assert [ax.get_visible() for ax in flat] == [True] * 5 + [False]


def test_8_the_shared_y_range_covers_every_panel():
    _fresh()
    fig, axes = small_multiples(_series(4), 2)
    fig.canvas.draw()
    lo, hi = axes[0, 0].get_ylim()
    assert lo <= 0 and hi >= 5
    assert axes[1, 1].get_ylim() == (lo, hi)


# ---- 9-14: twin_axis_chart ----


def test_9_two_axes_in_the_figure():
    _fresh()
    fig, left, right = twin_axis_chart([0, 1, 2], [1, 2, 3], [30, 20, 10], "revenue", "rate")
    assert left in fig.axes and right in fig.axes and left is not right
    assert len(fig.axes) == 2


def test_10_the_x_axis_is_shared():
    _fresh()
    _, left, right = twin_axis_chart([0, 1], [1, 2], [3, 4], "a", "b")
    assert _shared_x(left, right)
    assert not _shared_y(left, right)


def test_11_each_axes_has_its_own_line_and_colour():
    _fresh()
    _, left, right = twin_axis_chart([0, 1, 2], [1, 2, 3], [30, 20, 10], "a", "b")
    assert len(left.lines) == 1 and len(right.lines) == 1
    assert left.lines[0].get_ydata().tolist() == [1, 2, 3]
    assert right.lines[0].get_ydata().tolist() == [30, 20, 10]
    assert to_hex(left.lines[0].get_color()) == to_hex("tab:blue")
    assert to_hex(right.lines[0].get_color()) == to_hex("tab:red")


def test_12_labels_are_set():
    _fresh()
    _, left, right = twin_axis_chart([0, 1], [1, 2], [3, 4], "revenue (EUR)", "conversion (%)")
    assert left.get_ylabel() == "revenue (EUR)"
    assert right.get_ylabel() == "conversion (%)"


def test_13_label_colours_match_their_lines():
    _fresh()
    _, left, right = twin_axis_chart([0, 1], [1, 2], [3, 4], "a", "b")
    assert to_hex(left.yaxis.label.get_color()) == to_hex("tab:blue")
    assert to_hex(right.yaxis.label.get_color()) == to_hex("tab:red")


def test_14_the_second_y_axis_is_on_the_right():
    _fresh()
    _, left, right = twin_axis_chart([0, 1], [1, 2], [3, 4], "a", "b")
    assert right.yaxis.get_label_position() == "right"
    assert left.yaxis.get_label_position() == "left"


# ---- 15-17: set_limits_and_ticks ----


def test_15_limits_are_applied():
    _fresh()
    _, ax = plt.subplots()
    ax.plot([0, 1], [1, 2])
    set_limits_and_ticks(ax, (-1, 5), (0.5, 10), [0, 2, 4], ["a", "b", "c"], False)
    assert ax.get_xlim() == (-1, 5)
    assert ax.get_ylim() == (0.5, 10)


def test_16_ticks_and_their_labels():
    _fresh()
    _, ax = plt.subplots()
    ax.plot([0, 1], [1, 2])
    set_limits_and_ticks(ax, (0, 4), (0, 3), [0, 2, 4], ["zero", "two", "four"], False)
    assert ax.get_xticks().tolist() == [0, 2, 4]
    assert [t.get_text() for t in ax.get_xticklabels()] == ["zero", "two", "four"]


def test_17_log_scale_only_when_asked():
    _fresh()
    _, ax = plt.subplots()
    ax.plot([0, 1], [1, 100])
    set_limits_and_ticks(ax, (0, 1), (1, 100), [0, 1], ["a", "b"], True)
    assert ax.get_yscale() == "log"
    set_limits_and_ticks(ax, (0, 1), (1, 100), [0, 1], ["a", "b"], False)
    assert ax.get_yscale() == "linear"
