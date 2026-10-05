"""
pytest tests.py
"""

import math

import numpy as np
import pandas as pd
import pytest

from _load import load_solution

_module = load_solution(__file__)
revenue_pivot = _module.revenue_pivot
add_totals = _module.add_totals
count_table = _module.count_table
row_percentages = _module.row_percentages
to_long = _module.to_long


def _sales():
    return pd.DataFrame(
        {
            "region": ["south", "north", "north", "south", "north", "east"],
            "quarter": ["Q2", "Q1", "Q1", "Q1", "Q3", "Q2"],
            "revenue": [10, 5, 7, 20, 3, 8],
        }
    )


def _cell(grid, r, c):
    return grid.loc[r, c]


# ---- 1-5: revenue_pivot ----


def test_1_regions_down_quarters_across_both_sorted():
    grid = revenue_pivot(_sales())
    assert grid.index.tolist() == ["east", "north", "south"]
    assert grid.columns.tolist() == ["Q1", "Q2", "Q3"]


def test_2_duplicate_pairs_are_summed_not_averaged():
    grid = revenue_pivot(_sales())
    assert _cell(grid, "north", "Q1") == 12


def test_3_empty_cells_are_zero():
    grid = revenue_pivot(_sales())
    assert _cell(grid, "east", "Q1") == 0
    assert _cell(grid, "south", "Q3") == 0


def test_4_the_grand_total_equals_the_total_revenue():
    assert revenue_pivot(_sales()).to_numpy().sum() == 53


def test_5_matches_a_python_reference():
    rng = np.random.default_rng(2)
    df = pd.DataFrame(
        {"region": rng.choice(list("abcd"), size=50), "quarter": rng.choice(["Q1", "Q2", "Q3", "Q4"], size=50), "revenue": rng.integers(1, 20, size=50)}
    )
    grid = revenue_pivot(df)
    for r in grid.index:
        for c in grid.columns:
            assert _cell(grid, r, c) == df[(df["region"] == r) & (df["quarter"] == c)]["revenue"].sum()


# ---- 6-8: add_totals ----


def test_6_adds_a_total_row_and_column_with_the_grand_total_in_the_corner():
    grid = pd.DataFrame([[1, 2], [3, 4]], index=["a", "b"], columns=["x", "y"])
    out = add_totals(grid)
    assert out.index.tolist() == ["a", "b", "Total"]
    assert out.columns.tolist() == ["x", "y", "Total"]
    assert out.loc["a", "Total"] == 3 and out.loc["b", "Total"] == 7
    assert out.loc["Total", "x"] == 4 and out.loc["Total", "y"] == 6
    assert out.loc["Total", "Total"] == 10


def test_7_the_input_grid_is_not_changed():
    grid = pd.DataFrame([[1, 2], [3, 4]], index=["a", "b"], columns=["x", "y"])
    before = grid.copy()
    add_totals(grid)
    pd.testing.assert_frame_equal(grid, before)


def test_8_works_on_the_pivot_output():
    out = add_totals(revenue_pivot(_sales()))
    assert out.loc["Total", "Total"] == 53


# ---- 9-11: count_table ----


def test_9_counts_every_pair_with_sorted_axes():
    df = pd.DataFrame({"plan": ["b", "a", "b", "b"], "region": ["n", "n", "s", "n"]})
    t = count_table(df, "plan", "region")
    assert t.index.tolist() == ["a", "b"]
    assert t.columns.tolist() == ["n", "s"]
    assert t.loc["b", "n"] == 2 and t.loc["a", "s"] == 0


def test_10_cells_sum_to_the_number_of_rows():
    df = pd.DataFrame({"a": list("xyxyxy"), "b": list("ppqqrr")})
    assert count_table(df, "a", "b").to_numpy().sum() == 6


def test_11_counts_are_integers():
    df = pd.DataFrame({"a": list("xy"), "b": list("pq")})
    assert count_table(df, "a", "b").to_numpy().dtype.kind == "i"


# ---- 12-14: row_percentages ----


def test_12_each_row_sums_to_100():
    t = pd.DataFrame([[1, 3], [2, 2]], index=["a", "b"], columns=["x", "y"])
    out = row_percentages(t)
    assert out.loc["a"].tolist() == [25.0, 75.0]
    assert out.sum(axis=1).tolist() == [100.0, 100.0]


def test_13_a_zero_row_becomes_nan():
    t = pd.DataFrame([[0, 0], [1, 1]], index=["a", "b"], columns=["x", "y"])
    out = row_percentages(t)
    assert out.loc["a"].isna().all()
    assert out.loc["b"].tolist() == [50.0, 50.0]


def test_14_keeps_labels_and_does_not_change_the_input():
    t = pd.DataFrame([[1, 1]], index=["a"], columns=["x", "y"])
    before = t.copy()
    out = row_percentages(t)
    assert out.index.tolist() == ["a"] and out.columns.tolist() == ["x", "y"]
    pd.testing.assert_frame_equal(t, before)


# ---- 15-17: to_long ----


def _wide():
    return pd.DataFrame({"city": ["Pune", "Goa", "Agra"], "jan": [1, 2, 3], "feb": [4, 5, 6], "mar": [7, 8, 9]})


def test_15_columns_and_size():
    out = to_long(_wide(), "city", "month", "sales")
    assert out.columns.tolist() == ["city", "month", "sales"]
    assert len(out) == 9
    assert out.index.tolist() == list(range(9))


def test_16_rows_are_grouped_by_id_in_the_original_order_then_column_order():
    out = to_long(_wide(), "city", "month", "sales")
    assert out["city"].tolist() == ["Pune"] * 3 + ["Goa"] * 3 + ["Agra"] * 3
    assert out["month"].tolist() == ["jan", "feb", "mar"] * 3
    assert out["sales"].tolist() == [1, 4, 7, 2, 5, 8, 3, 6, 9]


def test_17_round_trips_through_a_pivot():
    out = to_long(_wide(), "city", "month", "sales")
    back = out.pivot(index="city", columns="month", values="sales")
    for city, row in _wide().set_index("city").iterrows():
        for month in ["jan", "feb", "mar"]:
            assert back.loc[city, month] == row[month]
