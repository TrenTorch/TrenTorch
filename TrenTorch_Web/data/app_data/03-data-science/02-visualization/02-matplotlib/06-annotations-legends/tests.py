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
annotate_max = _module.annotate_max
add_threshold = _module.add_threshold
shade_region = _module.shade_region
legend_below = _module.legend_below


def _fresh():
    plt.close("all")


def _x_extent(patch):
    # axvspan returns a Polygon in older matplotlib and a Rectangle in newer ones.
    if hasattr(patch, "get_width"):
        return [patch.get_x(), patch.get_x() + patch.get_width()]
    return patch.get_xy()[:, 0].tolist()


# ---- 1-6: annotate_max ----


def test_1_points_at_the_largest_value():
    _fresh()
    _, ax = plt.subplots()
    x, y = [1, 2, 3, 4], [3.0, 9.5, 4.0, 1.0]
    ann = annotate_max(ax, x, y)
    assert tuple(ann.xy) == (2, 9.5)


def test_2_the_text_reports_the_maximum():
    _fresh()
    _, ax = plt.subplots()
    ann = annotate_max(ax, [0, 1, 2], [1.0, 7.25, 3.0])
    assert ann.get_text() == "max = 7.25"
    ann2 = annotate_max(ax, [0, 1], [4, 10])
    assert ann2.get_text() == "max = 10"


def test_3_the_note_is_offset_twenty_points_above_with_an_arrow():
    _fresh()
    _, ax = plt.subplots()
    ann = annotate_max(ax, [0, 1], [1, 2])
    assert ann.xyann == (0, 20)
    assert ann.arrow_patch is not None


def test_4_ties_go_to_the_first_maximum():
    _fresh()
    _, ax = plt.subplots()
    ann = annotate_max(ax, [10, 20, 30], [5, 9, 9])
    assert tuple(ann.xy) == (20, 9)


def test_5_it_is_registered_on_the_axes():
    _fresh()
    _, ax = plt.subplots()
    ann = annotate_max(ax, [0, 1], [1, 2])
    assert ann in ax.texts


def test_6_works_with_numpy_input_and_negative_values():
    _fresh()
    _, ax = plt.subplots()
    ann = annotate_max(ax, np.array([0, 1, 2]), np.array([-5.0, -2.0, -9.0]))
    assert tuple(ann.xy) == (1, -2.0)
    assert ann.get_text() == "max = -2"


# ---- 7-11: add_threshold ----


def test_7_draws_a_horizontal_line_at_the_value():
    _fresh()
    _, ax = plt.subplots()
    line = add_threshold(ax, 50, "target")
    assert line in ax.lines
    assert list(line.get_ydata()) == [50, 50]


def test_8_style_and_label():
    _fresh()
    _, ax = plt.subplots()
    line = add_threshold(ax, 3.5, "limit")
    assert to_hex(line.get_color()) == to_hex("gray")
    assert line.get_linestyle() == "--"
    assert line.get_label() == "limit"


def test_9_the_legend_shows_the_label():
    _fresh()
    _, ax = plt.subplots()
    add_threshold(ax, 1, "goal")
    assert [t.get_text() for t in ax.get_legend().get_texts()] == ["goal"]


def test_10_it_does_not_disturb_other_lines():
    _fresh()
    _, ax = plt.subplots()
    ax.plot([0, 1, 2], [1, 2, 3])
    add_threshold(ax, 2, "t")
    assert len(ax.lines) == 2
    assert ax.lines[0].get_ydata().tolist() == [1, 2, 3]


def test_11_two_thresholds_both_appear_in_the_legend():
    _fresh()
    _, ax = plt.subplots()
    add_threshold(ax, 1, "low")
    add_threshold(ax, 9, "high")
    assert [t.get_text() for t in ax.get_legend().get_texts()] == ["low", "high"]


# ---- 12-14: shade_region ----


def test_12_covers_the_band_between_the_two_x_values():
    _fresh()
    _, ax = plt.subplots()
    patch = shade_region(ax, 2.0, 5.0, "campaign")
    xs = _x_extent(patch)
    assert min(xs) == pytest.approx(2.0) and max(xs) == pytest.approx(5.0)


def test_13_style_and_label():
    _fresh()
    _, ax = plt.subplots()
    patch = shade_region(ax, 0, 1, "window")
    assert patch.get_alpha() == pytest.approx(0.2)
    assert to_hex(patch.get_facecolor()[:3]) == to_hex("orange")
    assert patch.get_label() == "window"


def test_14_the_patch_is_added_to_the_axes():
    _fresh()
    _, ax = plt.subplots()
    patch = shade_region(ax, 0, 1, "w")
    assert patch in ax.patches


# ---- 15-17: legend_below ----


def test_15_title_columns_and_entries():
    _fresh()
    _, ax = plt.subplots()
    ax.plot([0, 1], [0, 1], label="a")
    ax.plot([0, 1], [1, 0], label="b")
    ax.plot([0, 1], [0.5, 0.5], label="c")
    legend = legend_below(ax, "Series")
    assert legend is ax.get_legend()
    assert legend.get_title().get_text() == "Series"
    assert [t.get_text() for t in legend.get_texts()] == ["a", "b", "c"]
    assert legend._ncols == 2


def test_16_it_is_anchored_below_the_axes():
    _fresh()
    fig, ax = plt.subplots()
    ax.plot([0, 1], [0, 1], label="a")
    legend = legend_below(ax, "S")
    fig.canvas.draw()
    legend_box = legend.get_window_extent()
    axes_box = ax.get_window_extent()
    assert legend_box.y1 <= axes_box.y0 + 1


def test_17_it_is_horizontally_centred_on_the_axes():
    _fresh()
    fig, ax = plt.subplots()
    ax.plot([0, 1], [0, 1], label="a")
    legend = legend_below(ax, "S")
    fig.canvas.draw()
    centre_legend = (legend.get_window_extent().x0 + legend.get_window_extent().x1) / 2
    centre_axes = (ax.get_window_extent().x0 + ax.get_window_extent().x1) / 2
    assert centre_legend == pytest.approx(centre_axes, abs=2)
