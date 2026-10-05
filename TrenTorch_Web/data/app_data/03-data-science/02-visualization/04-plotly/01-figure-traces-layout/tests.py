"""
pytest tests.py
"""

import numpy as np
import plotly.graph_objects as go

from _load import load_solution

_module = load_solution(__file__)
line_figure = _module.line_figure
add_series = _module.add_series
trace_summaries = _module.trace_summaries
set_axis_ranges = _module.set_axis_ranges
json_roundtrip = _module.json_roundtrip


def _fig():
    return line_figure([1, 2, 3], [4.0, 5.0, 7.0], "revenue", "Monthly revenue", "Month", "EUR")


# ---- 1-6: line_figure ----


def test_1_returns_a_figure_with_one_trace():
    fig = _fig()
    assert isinstance(fig, go.Figure)
    assert len(fig.data) == 1


def test_2_the_trace_is_a_scatter_through_the_points():
    trace = _fig().data[0]
    assert trace.type == "scatter"
    assert list(trace.x) == [1, 2, 3]
    assert list(trace.y) == [4.0, 5.0, 7.0]


def test_3_mode_and_name():
    trace = _fig().data[0]
    assert trace.mode == "lines+markers"
    assert trace.name == "revenue"


def test_4_layout_title_and_axis_titles():
    layout = _fig().layout
    assert layout.title.text == "Monthly revenue"
    assert layout.xaxis.title.text == "Month"
    assert layout.yaxis.title.text == "EUR"


def test_5_accepts_numpy_arrays():
    fig = line_figure(np.arange(4), np.arange(4) ** 2, "sq", "t", "x", "y")
    assert list(fig.data[0].y) == [0, 1, 4, 9]


def test_6_each_call_returns_an_independent_figure():
    a, b = _fig(), _fig()
    assert a is not b
    a.update_layout(title="changed")
    assert b.layout.title.text == "Monthly revenue"


# ---- 7-10: add_series ----


def test_7_returns_the_same_figure_object():
    fig = _fig()
    assert add_series(fig, [1, 2, 3], [1, 1, 1], "target", "red") is fig


def test_8_adds_a_lines_only_trace_with_name_and_colour():
    fig = add_series(_fig(), [1, 2, 3], [6, 6, 6], "target", "red")
    assert len(fig.data) == 2
    added = fig.data[1]
    assert added.mode == "lines" and added.name == "target"
    assert added.line.color == "red"
    assert list(added.y) == [6, 6, 6]


def test_9_the_first_trace_is_unchanged():
    fig = add_series(_fig(), [1], [1], "t", "blue")
    assert fig.data[0].name == "revenue" and fig.data[0].mode == "lines+markers"


def test_10_several_series_keep_their_order():
    fig = _fig()
    add_series(fig, [1], [1], "a", "red")
    add_series(fig, [1], [2], "b", "green")
    assert [t.name for t in fig.data] == ["revenue", "a", "b"]


# ---- 11-13: trace_summaries ----


def test_11_one_summary_per_trace_in_order():
    fig = add_series(_fig(), [1, 2], [3, 4], "target", "red")
    assert trace_summaries(fig) == [
        {"name": "revenue", "type": "scatter", "n_points": 3},
        {"name": "target", "type": "scatter", "n_points": 2},
    ]


def test_12_reports_other_trace_types():
    fig = go.Figure(data=[go.Bar(x=["a", "b", "c", "d"], y=[1, 2, 3, 4], name="bars")])
    assert trace_summaries(fig) == [{"name": "bars", "type": "bar", "n_points": 4}]


def test_13_an_empty_figure_has_no_summaries():
    assert trace_summaries(go.Figure()) == []


# ---- 14-15: set_axis_ranges ----


def test_14_ranges_are_set_on_both_axes_and_the_same_figure_returned():
    fig = _fig()
    out = set_axis_ranges(fig, (0, 10), (-1, 20))
    assert out is fig
    assert list(fig.layout.xaxis.range) == [0, 10]
    assert list(fig.layout.yaxis.range) == [-1, 20]


def test_15_setting_ranges_does_not_touch_the_traces_or_titles():
    fig = set_axis_ranges(_fig(), [0, 5], [0, 9])
    assert list(fig.data[0].y) == [4.0, 5.0, 7.0]
    assert fig.layout.title.text == "Monthly revenue"


# ---- 16-17: json_roundtrip ----


def test_16_the_copy_is_a_new_but_equal_figure():
    fig = add_series(_fig(), [1, 2, 3], [6, 6, 6], "target", "red")
    copy = json_roundtrip(fig)
    assert copy is not fig and isinstance(copy, go.Figure)
    assert copy.layout.title.text == "Monthly revenue"
    assert [t.name for t in copy.data] == ["revenue", "target"]
    assert list(copy.data[0].y) == [4.0, 5.0, 7.0]


def test_17_changing_the_copy_does_not_change_the_original():
    fig = _fig()
    copy = json_roundtrip(fig)
    copy.update_layout(title="other")
    assert fig.layout.title.text == "Monthly revenue"
