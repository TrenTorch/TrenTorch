"""
pytest tests.py
"""

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
import pytest

from _load import load_solution

_module = load_solution(__file__)
bar_chart = _module.bar_chart
grouped_bars = _module.grouped_bars
stacked_bars = _module.stacked_bars
annotate_bars = _module.annotate_bars


def _fresh():
    plt.close("all")


def _centre(p):
    return p.get_x() + p.get_width() / 2


def _ticklabels(ax):
    return [t.get_text() for t in ax.get_xticklabels()]


# ---- 1-5: bar_chart ----


def test_1_one_bar_per_value_with_the_right_heights():
    _fresh()
    _, ax = bar_chart(["a", "b", "c"], [3, 5, 2])
    assert [p.get_height() for p in ax.patches] == [3, 5, 2]


def test_2_bars_are_centred_at_integer_positions_with_default_width():
    _fresh()
    _, ax = bar_chart(["a", "b", "c"], [3, 5, 2])
    assert [_centre(p) for p in ax.patches] == pytest.approx([0, 1, 2])
    assert all(p.get_width() == pytest.approx(0.8) for p in ax.patches)


def test_3_ticks_are_at_the_positions_and_carry_the_labels():
    _fresh()
    _, ax = bar_chart(["mon", "tue", "wed"], [1, 2, 3])
    assert ax.get_xticks().tolist() == [0, 1, 2]
    assert _ticklabels(ax) == ["mon", "tue", "wed"]


def test_4_the_y_axis_starts_at_zero():
    _fresh()
    _, ax = bar_chart(["a", "b"], [50, 60])
    assert ax.get_ylim()[0] == 0


def test_5_returns_a_figure_containing_the_axes():
    _fresh()
    fig, ax = bar_chart(["a"], [1])
    assert fig.axes == [ax]


# ---- 6-10: grouped_bars ----


def _series():
    return {"2023": [10, 20, 30], "2024": [12, 18, 35]}


def test_6_one_bar_per_category_and_series():
    _fresh()
    _, ax = grouped_bars(["x", "y", "z"], _series())
    assert len(ax.patches) == 6
    heights = sorted(p.get_height() for p in ax.patches)
    assert heights == sorted([10, 20, 30, 12, 18, 35])


def test_7_each_bar_has_width_point_eight_over_k():
    _fresh()
    _, ax = grouped_bars(["x", "y", "z"], _series())
    assert all(p.get_width() == pytest.approx(0.4) for p in ax.patches)


def test_8_bars_are_offset_symmetrically_around_each_tick():
    _fresh()
    _, ax = grouped_bars(["x", "y", "z"], _series())
    first_series = [_centre(p) for p in ax.patches[:3]]
    second_series = [_centre(p) for p in ax.patches[3:]]
    assert first_series == pytest.approx([-0.2, 0.8, 1.8])
    assert second_series == pytest.approx([0.2, 1.2, 2.2])


def test_9_three_series_are_centred_on_the_tick():
    _fresh()
    _, ax = grouped_bars(["x", "y"], {"a": [1, 1], "b": [2, 2], "c": [3, 3]})
    width = 0.8 / 3
    # patches are in series-major order: 0-1 series a, 2-3 series b, 4-5 series c
    assert [_centre(ax.patches[i]) for i in (0, 2, 4)] == pytest.approx([-width, 0.0, width])


def test_10_legend_lists_the_series_and_ticks_the_labels():
    _fresh()
    _, ax = grouped_bars(["x", "y", "z"], _series())
    assert [t.get_text() for t in ax.get_legend().get_texts()] == ["2023", "2024"]
    assert _ticklabels(ax) == ["x", "y", "z"]


# ---- 11-14: stacked_bars ----


def test_11_series_start_where_the_previous_ones_end():
    _fresh()
    _, ax = stacked_bars(["x", "y"], {"a": [1, 2], "b": [3, 4], "c": [5, 6]})
    bottoms = [p.get_y() for p in ax.patches]
    assert bottoms == pytest.approx([0, 0, 1, 2, 4, 6])


def test_12_heights_are_the_series_values_and_width_is_point_six():
    _fresh()
    _, ax = stacked_bars(["x", "y"], {"a": [1, 2], "b": [3, 4]})
    assert [p.get_height() for p in ax.patches] == [1, 2, 3, 4]
    assert all(p.get_width() == pytest.approx(0.6) for p in ax.patches)
    assert [_centre(p) for p in ax.patches] == pytest.approx([0, 1, 0, 1])


def test_13_the_total_height_of_each_stack_is_the_sum():
    _fresh()
    series = {"a": [1, 2], "b": [3, 4], "c": [5, 6]}
    _, ax = stacked_bars(["x", "y"], series)
    tops = [p.get_y() + p.get_height() for p in ax.patches]
    assert tops[-2] == pytest.approx(9) and tops[-1] == pytest.approx(12)


def test_14_legend_and_tick_labels():
    _fresh()
    _, ax = stacked_bars(["x", "y"], {"a": [1, 2], "b": [3, 4]})
    assert [t.get_text() for t in ax.get_legend().get_texts()] == ["a", "b"]
    assert _ticklabels(ax) == ["x", "y"]


# ---- 15-17: annotate_bars ----


def test_15_returns_the_formatted_heights_in_patch_order():
    _fresh()
    _, ax = bar_chart(["a", "b", "c"], [3, 5.5, 2.25])
    assert annotate_bars(ax) == ["3", "5.5", "2.25"]


def test_16_writes_one_text_per_bar_at_the_top_centre():
    _fresh()
    _, ax = bar_chart(["a", "b"], [4, 9])
    annotate_bars(ax)
    assert len(ax.texts) == 2
    positions = sorted((t.get_position() for t in ax.texts))
    assert positions[0] == pytest.approx((0, 4)) and positions[1] == pytest.approx((1, 9))
    assert all(t.get_ha() == "center" for t in ax.texts)


def test_17_stacked_bars_are_labelled_at_their_own_top_with_their_own_height():
    _fresh()
    _, ax = stacked_bars(["x"], {"a": [2], "b": [3]})
    assert annotate_bars(ax) == ["2", "3"]
    assert sorted(t.get_position()[1] for t in ax.texts) == pytest.approx([2, 5])
