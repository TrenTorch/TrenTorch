"""
pytest tests.py
"""

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
from matplotlib.colors import to_hex
from matplotlib.figure import Figure
from matplotlib.lines import Line2D

from _load import load_solution

_module = load_solution(__file__)
line_chart = _module.line_chart
add_line = _module.add_line
line_data = _module.line_data
style_line = _module.style_line


def _fresh():
    plt.close("all")


# ---- 1-6: line_chart ----


def test_1_returns_a_figure_and_one_axes_that_belongs_to_it():
    _fresh()
    fig, ax = line_chart([1, 2, 3], [4, 5, 6], "t", "x", "y")
    assert isinstance(fig, Figure)
    assert fig.axes == [ax]


def test_2_draws_exactly_one_line_through_the_points():
    _fresh()
    _, ax = line_chart([1, 2, 3], [4, 5, 7], "t", "x", "y")
    assert len(ax.lines) == 1
    assert ax.lines[0].get_xydata().tolist() == [[1, 4], [2, 5], [3, 7]]


def test_3_title_and_axis_labels_are_set():
    _fresh()
    _, ax = line_chart([0, 1], [0, 1], "Revenue", "Month", "Euros")
    assert ax.get_title() == "Revenue"
    assert ax.get_xlabel() == "Month"
    assert ax.get_ylabel() == "Euros"


def test_4_the_grid_is_on():
    _fresh()
    _, ax = line_chart([0, 1], [0, 1], "t", "x", "y")
    assert ax.xaxis.get_gridlines()[0].get_visible()
    assert ax.yaxis.get_gridlines()[0].get_visible()


def test_5_each_call_makes_a_new_figure():
    _fresh()
    f1, _ = line_chart([0, 1], [0, 1], "a", "x", "y")
    f2, _ = line_chart([0, 1], [0, 1], "b", "x", "y")
    assert f1 is not f2
    assert len(plt.get_fignums()) == 2


def test_6_accepts_numpy_arrays():
    _fresh()
    x = np.linspace(0, 1, 5)
    _, ax = line_chart(x, x**2, "sq", "x", "y")
    assert np.allclose(ax.lines[0].get_ydata(), x**2)


# ---- 7-11: add_line ----


def test_7_adds_a_second_line_with_its_label_and_colour():
    _fresh()
    _, ax = line_chart([0, 1, 2], [0, 1, 2], "t", "x", "y")
    line = add_line(ax, [0, 1, 2], [2, 1, 0], "down", "red")
    assert isinstance(line, Line2D)
    assert len(ax.lines) == 2
    assert line.get_label() == "down"
    assert to_hex(line.get_color()) == to_hex("red")


def test_8_the_legend_lists_only_labelled_lines():
    _fresh()
    _, ax = line_chart([0, 1], [0, 1], "t", "x", "y")
    add_line(ax, [0, 1], [1, 0], "second", "green")
    legend = ax.get_legend()
    assert legend is not None
    assert [t.get_text() for t in legend.get_texts()] == ["second"]


def test_9_works_on_any_axes_not_just_the_current_one():
    _fresh()
    fig, axes = plt.subplots(1, 2)
    add_line(axes[0], [0, 1], [0, 1], "a", "blue")
    assert len(axes[0].lines) == 1 and len(axes[1].lines) == 0


def test_10_the_new_line_has_the_given_data():
    _fresh()
    _, ax = plt.subplots()
    line = add_line(ax, [1, 2], [10, 20], "d", "k")
    assert line.get_ydata().tolist() == [10, 20]


def test_11_a_second_added_line_extends_the_legend():
    _fresh()
    _, ax = plt.subplots()
    add_line(ax, [0, 1], [0, 1], "one", "r")
    add_line(ax, [0, 1], [1, 0], "two", "b")
    assert [t.get_text() for t in ax.get_legend().get_texts()] == ["one", "two"]


# ---- 12-14: line_data ----


def test_12_returns_lists_in_drawing_order():
    _fresh()
    _, ax = plt.subplots()
    ax.plot([1, 2], [3, 4])
    ax.plot([5, 6, 7], [8, 9, 10])
    data = line_data(ax)
    assert data == [([1, 2], [3, 4]), ([5, 6, 7], [8, 9, 10])]


def test_13_values_are_python_lists_of_numbers():
    _fresh()
    _, ax = plt.subplots()
    ax.plot(np.arange(3), np.arange(3) * 2.0)
    xs, ys = line_data(ax)[0]
    assert type(xs) is list and type(ys) is list
    assert ys == [0.0, 2.0, 4.0]


def test_14_an_axes_without_lines_gives_an_empty_list():
    _fresh()
    _, ax = plt.subplots()
    assert line_data(ax) == []


# ---- 15-17: style_line ----


def test_15_changes_the_four_properties():
    _fresh()
    _, ax = plt.subplots()
    (line,) = ax.plot([0, 1], [0, 1])
    out = style_line(line, "purple", "--", 3.5, "o")
    assert out is line
    assert to_hex(line.get_color()) == to_hex("purple")
    assert line.get_linestyle() == "--"
    assert line.get_linewidth() == 3.5
    assert line.get_marker() == "o"


def test_16_does_not_add_a_line_or_move_the_data():
    _fresh()
    _, ax = plt.subplots()
    (line,) = ax.plot([1, 2, 3], [4, 5, 6])
    style_line(line, "k", ":", 1.0, "s")
    assert len(ax.lines) == 1
    assert line.get_xydata().tolist() == [[1, 4], [2, 5], [3, 6]]


def test_17_only_the_given_line_is_changed():
    _fresh()
    _, ax = plt.subplots()
    (a,) = ax.plot([0, 1], [0, 1], color="red")
    (b,) = ax.plot([0, 1], [1, 0], color="blue")
    style_line(a, "green", "-", 2.0, "x")
    assert to_hex(b.get_color()) == to_hex("blue")
