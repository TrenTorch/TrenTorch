"""
pytest tests.py
"""

import pandas as pd
import plotly.graph_objects as go
import pytest

from _load import load_solution

_module = load_solution(__file__)
stacked_panels = _module.stacked_panels
facet_scatter = _module.facet_scatter
panel_titles = _module.panel_titles


def _frame():
    return pd.DataFrame(
        {
            "x": [1, 2, 3, 4, 5, 6],
            "y": [10.0, 11.0, 12.0, 13.0, 14.0, 15.0],
            "region": ["west", "east", "north", "west", "east", "north"],
        }
    )


# ---- 1-8: stacked_panels ----


def test_1_two_scatter_traces():
    fig = stacked_panels([1, 2, 3], [1, 2, 3], [9, 8, 7], ("Price", "Volume"))
    assert isinstance(fig, go.Figure)
    assert [t.type for t in fig.data] == ["scatter", "scatter"]


def test_2_each_trace_holds_its_series():
    fig = stacked_panels([1, 2, 3], [1, 2, 3], [9, 8, 7], ("Price", "Volume"))
    assert list(fig.data[0].y) == [1, 2, 3]
    assert list(fig.data[1].y) == [9, 8, 7]
    assert list(fig.data[0].x) == [1, 2, 3] and list(fig.data[1].x) == [1, 2, 3]


def test_3_the_first_trace_is_in_the_first_panel_and_the_second_in_the_second():
    fig = stacked_panels([1, 2], [1, 2], [3, 4], ("a", "b"))
    assert (fig.data[0].xaxis, fig.data[0].yaxis) == ("x", "y")
    assert (fig.data[1].xaxis, fig.data[1].yaxis) == ("x2", "y2")


def test_4_the_panels_are_stacked_vertically():
    fig = stacked_panels([1, 2], [1, 2], [3, 4], ("a", "b"))
    top, bottom = fig.layout.yaxis.domain, fig.layout.yaxis2.domain
    assert top[0] > bottom[1]


def test_5_the_x_axes_are_linked_so_zooming_one_zooms_both():
    fig = stacked_panels([1, 2], [1, 2], [3, 4], ("a", "b"))
    # plotly links the upper panel's x axis to the bottom one's
    assert fig.layout.xaxis.matches == "x2"


def test_6_subplot_titles_are_set_in_order():
    fig = stacked_panels([1, 2], [1, 2], [3, 4], ("Price", "Volume"))
    assert panel_titles(fig) == ["Price", "Volume"]


def test_7_the_two_panels_share_the_full_width():
    fig = stacked_panels([1, 2], [1, 2], [3, 4], ("a", "b"))
    assert tuple(fig.layout.xaxis.domain) == tuple(fig.layout.xaxis2.domain) == (0.0, 1.0)


def test_8_accepts_a_list_of_titles_too():
    fig = stacked_panels([1], [1], [2], ["T1", "T2"])
    assert panel_titles(fig) == ["T1", "T2"]


# ---- 9-14: facet_scatter ----


def test_9_one_trace_and_one_panel_per_group():
    fig = facet_scatter(_frame(), "x", "y", "region", ["west", "east", "north"])
    assert len(fig.data) == 3
    assert len(panel_titles(fig)) == 3


def test_10_panels_follow_the_requested_order():
    fig = facet_scatter(_frame(), "x", "y", "region", ["north", "west", "east"])
    assert panel_titles(fig) == ["region=north", "region=west", "region=east"]


def test_11_each_panel_has_only_its_own_rows():
    df = _frame()
    fig = facet_scatter(df, "x", "y", "region", ["north", "west", "east"])
    for trace, region in zip(fig.data, ["north", "west", "east"]):
        assert list(trace.x) == df[df["region"] == region]["x"].tolist()


def test_12_panels_sit_side_by_side_in_that_order():
    fig = facet_scatter(_frame(), "x", "y", "region", ["north", "west", "east"])
    starts = [fig.layout.xaxis.domain[0], fig.layout.xaxis2.domain[0], fig.layout.xaxis3.domain[0]]
    assert starts == sorted(starts)


def test_13_the_traces_use_consecutive_axes():
    fig = facet_scatter(_frame(), "x", "y", "region", ["north", "west", "east"])
    assert [t.xaxis for t in fig.data] == ["x", "x2", "x3"]


def test_14_axis_titles_name_the_columns():
    fig = facet_scatter(_frame(), "x", "y", "region", ["north", "west", "east"])
    assert fig.layout.xaxis.title.text == "x"
    assert fig.layout.yaxis.title.text == "y"


# ---- 15-17: panel_titles ----


def test_15_a_figure_without_panels_has_no_titles():
    assert panel_titles(go.Figure()) == []


def test_16_returns_plain_strings_in_a_list():
    fig = stacked_panels([1], [1], [2], ("A", "B"))
    out = panel_titles(fig)
    assert type(out) is list and all(type(t) is str for t in out)


def test_17_other_annotations_are_listed_too_in_order():
    fig = stacked_panels([1], [1], [2], ("A", "B"))
    fig.add_annotation(text="note", x=1, y=1, showarrow=False)
    assert panel_titles(fig) == ["A", "B", "note"]
