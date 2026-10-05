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
ranked_order = _module.ranked_order
mean_bars = _module.mean_bars
count_bars = _module.count_bars
horizontal_means = _module.horizontal_means


def _fresh():
    plt.close("all")


def _frame():
    return pd.DataFrame(
        {
            "team": ["red", "blue", "red", "green", "blue", "green", "red", "blue", "green", "red"],
            "score": [4.0, 9.0, 6.0, 5.0, 7.0, np.nan, 2.0, 8.0, 5.0, 8.0],
            "tier": ["x", "y", "x", "x", "y", "y", "x", "x", "y", "y"],
        }
    )


def _labels(ax, axis="x"):
    ticks = ax.get_xticklabels() if axis == "x" else ax.get_yticklabels()
    return [t.get_text() for t in ticks]


# ---- 1-4: ranked_order ----


def test_1_largest_mean_first():
    assert ranked_order(_frame(), "team", "score") == ["blue", "green", "red"]


def test_2_ties_break_by_name_ascending():
    df = pd.DataFrame({"c": ["b", "a", "c", "a", "b", "c"], "v": [1, 5, 5, 5, 1, 5]})
    assert ranked_order(df, "c", "v") == ["a", "c", "b"]


def test_3_missing_values_are_ignored_in_the_mean():
    df = pd.DataFrame({"c": ["p", "p", "q", "q"], "v": [10.0, np.nan, 7.0, 8.0]})
    assert ranked_order(df, "c", "v") == ["p", "q"]


def test_4_returns_a_plain_list_of_the_categories():
    out = ranked_order(_frame(), "team", "score")
    assert type(out) is list and set(out) == {"red", "blue", "green"}


# ---- 5-9: mean_bars ----


def test_5_one_bar_per_category_in_the_requested_order():
    _fresh()
    ax = mean_bars(_frame(), "team", "score", ["red", "blue", "green"])
    assert _labels(ax) == ["red", "blue", "green"]
    assert len(ax.patches) == 3


def test_6_bar_heights_are_the_means():
    _fresh()
    df = _frame()
    ax = mean_bars(df, "team", "score", ["red", "blue", "green"])
    expected = df.groupby("team")["score"].mean()
    assert [p.get_height() for p in ax.patches] == pytest.approx([expected["red"], expected["blue"], expected["green"]])


def test_7_there_are_no_error_bars():
    _fresh()
    ax = mean_bars(_frame(), "team", "score", ["blue", "green", "red"])
    assert len(ax.lines) == 0


def test_8_axis_labels_name_the_columns():
    _fresh()
    ax = mean_bars(_frame(), "team", "score", ["blue", "green", "red"])
    assert ax.get_xlabel() == "team" and ax.get_ylabel() == "score"


def test_9_works_with_a_ranked_order():
    _fresh()
    df = _frame()
    order = ranked_order(df, "team", "score")
    ax = mean_bars(df, "team", "score", order)
    heights = [p.get_height() for p in ax.patches]
    assert heights == sorted(heights, reverse=True)


# ---- 10-13: count_bars ----


def test_10_one_container_per_hue_level_with_one_bar_per_category():
    _fresh()
    ax = count_bars(_frame(), "team", "tier", ["red", "blue", "green"], ["x", "y"])
    assert len(ax.containers) == 2
    assert all(len(c) == 3 for c in ax.containers)


def test_11_heights_are_the_row_counts():
    _fresh()
    df = _frame()
    order, hue_order = ["red", "blue", "green"], ["x", "y"]
    ax = count_bars(df, "team", "tier", order, hue_order)
    table = pd.crosstab(df["team"], df["tier"])
    for container, level in zip(ax.containers, hue_order):
        assert [b.get_height() for b in container] == [table.loc[t, level] for t in order]


def test_12_legend_follows_hue_order_and_categories_follow_order():
    _fresh()
    ax = count_bars(_frame(), "team", "tier", ["green", "red", "blue"], ["y", "x"])
    assert [t.get_text() for t in ax.get_legend().get_texts()] == ["y", "x"]
    assert _labels(ax) == ["green", "red", "blue"]


def test_13_total_bar_height_equals_the_number_of_rows():
    _fresh()
    ax = count_bars(_frame(), "team", "tier", ["red", "blue", "green"], ["x", "y"])
    assert sum(p.get_height() for p in ax.patches) == 10
    assert ax.get_ylabel() == "count"


# ---- 14-17: horizontal_means ----


def test_14_categories_are_on_the_y_axis_in_order():
    _fresh()
    ax = horizontal_means(_frame(), "team", "score", ["green", "red", "blue"])
    assert _labels(ax, "y") == ["green", "red", "blue"]


def test_15_bar_lengths_are_the_means():
    _fresh()
    df = _frame()
    ax = horizontal_means(df, "team", "score", ["green", "red", "blue"])
    expected = df.groupby("team")["score"].mean()
    assert [p.get_width() for p in ax.patches] == pytest.approx([expected["green"], expected["red"], expected["blue"]])


def test_16_there_are_no_error_bars():
    _fresh()
    ax = horizontal_means(_frame(), "team", "score", ["green", "red", "blue"])
    assert len(ax.lines) == 0


def test_17_axis_labels_are_swapped_relative_to_the_vertical_chart():
    _fresh()
    ax = horizontal_means(_frame(), "team", "score", ["green", "red", "blue"])
    assert ax.get_xlabel() == "score" and ax.get_ylabel() == "team"
