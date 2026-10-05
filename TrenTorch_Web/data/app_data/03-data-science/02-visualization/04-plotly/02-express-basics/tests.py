"""
pytest tests.py
"""

import numpy as np
import pandas as pd
import plotly.graph_objects as go
import pytest

from _load import load_solution

_module = load_solution(__file__)
scatter_by_group = _module.scatter_by_group
total_bars = _module.total_bars
histogram_figure = _module.histogram_figure
lines_by_group = _module.lines_by_group


def _frame():
    return pd.DataFrame(
        {
            "x": [5, 1, 3, 2, 4, 6, 1, 2],
            "y": [10.0, 20.0, 30.0, 40.0, 50.0, 60.0, 70.0, 80.0],
            "g": ["b", "a", "b", "c", "a", "c", "a", "b"],
        }
    )


# ---- 1-5: scatter_by_group ----


def test_1_one_trace_per_group():
    fig = scatter_by_group(_frame(), "x", "y", "g", ["a", "b", "c"])
    assert isinstance(fig, go.Figure)
    assert len(fig.data) == 3
    assert all(t.type == "scatter" for t in fig.data)


def test_2_traces_follow_the_requested_order():
    fig = scatter_by_group(_frame(), "x", "y", "g", ["c", "a", "b"])
    assert [t.name for t in fig.data] == ["c", "a", "b"]


def test_3_each_trace_holds_only_its_groups_points_in_row_order():
    df = _frame()
    fig = scatter_by_group(df, "x", "y", "g", ["a", "b", "c"])
    for trace in fig.data:
        subset = df[df["g"] == trace.name]
        assert list(trace.x) == subset["x"].tolist()
        assert list(trace.y) == subset["y"].tolist()


def test_4_axis_titles_are_the_column_names_and_the_legend_title_the_group():
    fig = scatter_by_group(_frame(), "x", "y", "g", ["a", "b", "c"])
    assert fig.layout.xaxis.title.text == "x"
    assert fig.layout.yaxis.title.text == "y"
    assert fig.layout.legend.title.text == "g"


def test_5_every_row_appears_exactly_once():
    fig = scatter_by_group(_frame(), "x", "y", "g", ["b", "c", "a"])
    assert sum(len(t.x) for t in fig.data) == 8


# ---- 6-10: total_bars ----


def test_6_one_bar_trace_with_one_bar_per_category():
    fig = total_bars(_frame(), "g", "y")
    assert len(fig.data) == 1 and fig.data[0].type == "bar"
    assert sorted(fig.data[0].x) == ["a", "b", "c"]


def test_7_heights_are_the_sums():
    fig = total_bars(_frame(), "g", "y")
    totals = dict(zip(fig.data[0].x, fig.data[0].y))
    assert totals == {"a": 140.0, "b": 120.0, "c": 100.0}


def test_8_largest_total_first():
    fig = total_bars(_frame(), "g", "y")
    assert list(fig.data[0].x) == ["a", "b", "c"]
    assert list(fig.data[0].y) == [140.0, 120.0, 100.0]


def test_9_ties_break_by_category_name():
    df = pd.DataFrame({"k": ["z", "a", "m", "a", "z", "m"], "v": [1, 5, 9, 5, 4, 1]})
    fig = total_bars(df, "k", "v")
    # totals: z=5, a=10, m=10 -> a and m tie, a first
    assert list(fig.data[0].x) == ["a", "m", "z"]


def test_10_it_aggregates_instead_of_drawing_one_bar_per_row():
    df = pd.DataFrame({"k": ["p"] * 5 + ["q"] * 5, "v": range(10)})
    assert len(total_bars(df, "k", "v").data[0].x) == 2


# ---- 11-13: histogram_figure ----


def test_11_a_histogram_trace_of_the_column():
    df = pd.DataFrame({"v": np.arange(40.0)})
    fig = histogram_figure(df, "v", 8)
    assert len(fig.data) == 1 and fig.data[0].type == "histogram"
    assert list(fig.data[0].x) == list(np.arange(40.0))


def test_12_it_requests_the_number_of_bins():
    df = pd.DataFrame({"v": np.arange(40.0)})
    assert histogram_figure(df, "v", 8).data[0].nbinsx == 8
    assert histogram_figure(df, "v", 15).data[0].nbinsx == 15


def test_13_axis_titles():
    df = pd.DataFrame({"score": [1, 2, 2, 3]})
    fig = histogram_figure(df, "score", 3)
    assert fig.layout.xaxis.title.text == "score"
    assert fig.layout.yaxis.title.text == "count"


# ---- 14-17: lines_by_group ----


def test_14_one_line_trace_per_group_in_order_of_first_appearance():
    fig = lines_by_group(_frame(), "x", "y", "g")
    assert [t.name for t in fig.data] == ["b", "a", "c"]
    assert all(t.mode == "lines" for t in fig.data)


def test_15_each_line_is_sorted_by_x():
    fig = lines_by_group(_frame(), "x", "y", "g")
    for trace in fig.data:
        xs = list(trace.x)
        assert xs == sorted(xs)


def test_16_each_line_keeps_its_groups_pairs_together():
    df = _frame()
    fig = lines_by_group(df, "x", "y", "g")
    for trace in fig.data:
        expected = df[df["g"] == trace.name].sort_values("x", kind="mergesort")
        assert list(trace.x) == expected["x"].tolist()
        assert list(trace.y) == expected["y"].tolist()


def test_17_the_input_frame_is_not_reordered():
    df = _frame()
    before = df.copy()
    lines_by_group(df, "x", "y", "g")
    pd.testing.assert_frame_equal(df, before)
