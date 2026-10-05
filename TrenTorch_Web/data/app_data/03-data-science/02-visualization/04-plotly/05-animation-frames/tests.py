"""
pytest tests.py
"""

import numpy as np
import pandas as pd
import plotly.graph_objects as go
import pytest

from _load import load_solution

_module = load_solution(__file__)
animated_scatter = _module.animated_scatter
figure_from_frames = _module.figure_from_frames
last_frame_summary = _module.last_frame_summary


def _frame():
    return pd.DataFrame(
        {
            "gdp": [1.0, 2.0, 3.0, 1.5, 2.5, 4.5, 2.0, 3.5, 6.0],
            "life": [50.0, 60.0, 70.0, 55.0, 62.0, 75.0, 58.0, 66.0, 80.0],
            "year": [2000, 2000, 2000, 2010, 2010, 2010, 2020, 2020, 2020],
        }
    )


def _frames():
    return {
        "a": ([1, 2, 3], [4, 5, 6]),
        "b": ([2, 3, 4, 5], [1, 1, 2, 2]),
        "c": ([9.5], [0.5]),
    }


# ---- 1-7: animated_scatter ----


def test_1_one_animation_frame_per_value_of_the_column():
    fig = animated_scatter(_frame(), "gdp", "life", "year")
    assert isinstance(fig, go.Figure)
    assert [f.name for f in fig.frames] == ["2000", "2010", "2020"]


def test_2_the_axes_are_fixed_to_the_whole_data_range():
    fig = animated_scatter(_frame(), "gdp", "life", "year")
    assert list(fig.layout.xaxis.range) == [1.0, 6.0]
    assert list(fig.layout.yaxis.range) == [50.0, 80.0]


def test_3_each_frame_holds_only_its_years_points():
    df = _frame()
    fig = animated_scatter(df, "gdp", "life", "year")
    for frame in fig.frames:
        subset = df[df["year"] == int(frame.name)]
        assert list(frame.data[0].x) == subset["gdp"].tolist()
        assert list(frame.data[0].y) == subset["life"].tolist()


def test_4_the_first_frame_is_the_initial_data():
    df = _frame()
    fig = animated_scatter(df, "gdp", "life", "year")
    assert list(fig.data[0].x) == df[df["year"] == 2000]["gdp"].tolist()


def test_5_there_is_a_slider_with_one_step_per_frame():
    fig = animated_scatter(_frame(), "gdp", "life", "year")
    assert len(fig.layout.sliders) == 1
    assert [s.label for s in fig.layout.sliders[0].steps] == ["2000", "2010", "2020"]


def test_6_the_ranges_use_all_frames_not_just_the_first():
    df = _frame()
    fig = animated_scatter(df, "gdp", "life", "year")
    first_only = df[df["year"] == 2000]["gdp"].max()
    assert fig.layout.xaxis.range[1] > first_only


def test_7_axis_titles_are_the_column_names():
    fig = animated_scatter(_frame(), "gdp", "life", "year")
    assert fig.layout.xaxis.title.text == "gdp" and fig.layout.yaxis.title.text == "life"


# ---- 8-14: figure_from_frames ----


def test_8_initial_data_is_the_first_entry_as_markers():
    fig = figure_from_frames(_frames())
    assert len(fig.data) == 1
    assert fig.data[0].type == "scatter" and fig.data[0].mode == "markers"
    assert list(fig.data[0].x) == [1, 2, 3] and list(fig.data[0].y) == [4, 5, 6]


def test_9_one_frame_per_entry_in_order_with_the_same_names():
    fig = figure_from_frames(_frames())
    assert [f.name for f in fig.frames] == ["a", "b", "c"]


def test_10_each_frame_holds_its_points():
    fig = figure_from_frames(_frames())
    assert list(fig.frames[1].data[0].x) == [2, 3, 4, 5]
    assert list(fig.frames[1].data[0].y) == [1, 1, 2, 2]
    assert list(fig.frames[2].data[0].x) == [9.5]


def test_11_a_slider_with_one_step_per_frame_in_order():
    fig = figure_from_frames(_frames())
    steps = fig.layout.sliders[0].steps
    assert [s.label for s in steps] == ["a", "b", "c"]


def test_12_every_step_animates_exactly_its_frame():
    fig = figure_from_frames(_frames())
    for step, frame in zip(fig.layout.sliders[0].steps, fig.frames):
        assert step.method == "animate"
        assert list(step.args[0]) == [frame.name]


def test_13_step_targets_match_frame_names_exactly():
    fig = figure_from_frames(_frames())
    names = {f.name for f in fig.frames}
    assert {s.args[0][0] for s in fig.layout.sliders[0].steps} == names


def test_14_a_single_entry_works():
    fig = figure_from_frames({"only": ([1, 2], [3, 4])})
    assert [f.name for f in fig.frames] == ["only"]
    assert len(fig.layout.sliders[0].steps) == 1


# ---- 15-17: last_frame_summary ----


def test_15_describes_the_last_frame():
    fig = figure_from_frames(_frames())
    assert last_frame_summary(fig) == {"name": "c", "n_points": 1, "x_max": 9.5}


def test_16_works_on_an_express_animation():
    fig = animated_scatter(_frame(), "gdp", "life", "year")
    out = last_frame_summary(fig)
    assert out == {"name": "2020", "n_points": 3, "x_max": 6.0}


def test_17_x_max_is_a_python_float_and_n_points_an_int():
    out = last_frame_summary(figure_from_frames({"f": ([1, 4, 2], [0, 0, 0])}))
    assert type(out["x_max"]) is float and out["x_max"] == 4.0
    assert type(out["n_points"]) is int and out["n_points"] == 3
