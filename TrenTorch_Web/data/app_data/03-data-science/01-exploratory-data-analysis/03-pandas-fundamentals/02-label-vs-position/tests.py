"""
pytest tests.py
"""

import numpy as np
import pandas as pd

from _load import load_solution

_module = load_solution(__file__)
rows_by_label = _module.rows_by_label
rows_by_position = _module.rows_by_position
cell = _module.cell
numeric_columns = _module.numeric_columns
with_value_where = _module.with_value_where


def _frame():
    # Labels are deliberately NOT 0..n-1, so label and position disagree.
    return pd.DataFrame(
        {"city": ["Pune", "Delhi", "Goa", "Agra", "Kochi"], "temp": [31, 38, 29, 40, 30], "ok": [True, False, True, False, True]},
        index=[10, 20, 30, 40, 50],
    )


# ---- 1-4: rows_by_label ----


def test_1_label_slice_includes_both_ends():
    out = rows_by_label(_frame(), 20, 40)
    assert out.index.tolist() == [20, 30, 40]


def test_2_label_slice_follows_the_frames_own_order():
    df = _frame().iloc[::-1]  # index 50, 40, 30, 20, 10
    assert rows_by_label(df, 40, 20).index.tolist() == [40, 30, 20]


def test_3_a_single_label_range_returns_one_row():
    assert rows_by_label(_frame(), 30, 30).index.tolist() == [30]


def test_4_works_with_string_labels():
    df = pd.DataFrame({"v": [1, 2, 3, 4]}, index=["mon", "tue", "wed", "thu"])
    assert rows_by_label(df, "tue", "wed")["v"].tolist() == [2, 3]


# ---- 5-8: rows_by_position ----


def test_5_position_slice_excludes_the_stop():
    assert rows_by_position(_frame(), 1, 3).index.tolist() == [20, 30]


def test_6_label_and_position_pick_different_rows_when_the_index_is_not_0_to_n():
    df = _frame()  # labels 10, 20, 30, 40, 50
    assert rows_by_position(df, 0, 2).index.tolist() == [10, 20]
    assert rows_by_label(df, 10, 20).index.tolist() == [10, 20]
    assert rows_by_position(df, 1, 3).index.tolist() == [20, 30]


def test_7_position_zero_to_n_is_everything():
    df = _frame()
    pd.testing.assert_frame_equal(rows_by_position(df, 0, len(df)), df)


def test_8_empty_slice_is_allowed():
    assert rows_by_position(_frame(), 2, 2).shape[0] == 0


# ---- 9-10: cell ----


def test_9_reads_one_value_by_labels():
    assert cell(_frame(), 30, "city") == "Goa"
    assert cell(_frame(), 40, "temp") == 40


def test_10_returns_a_scalar_not_a_series():
    value = cell(_frame(), 20, "temp")
    assert not isinstance(value, (pd.Series, pd.DataFrame))


# ---- 11-13: numeric_columns ----


def test_11_picks_ints_and_floats_only():
    df = pd.DataFrame({"a": [1, 2], "b": [1.5, 2.5], "c": ["x", "y"], "d": [True, False]})
    assert numeric_columns(df) == ["a", "b"]


def test_12_keeps_column_order():
    df = pd.DataFrame({"z": [1.0], "a": [2], "m": ["t"], "b": [3.0]})
    assert numeric_columns(df) == ["z", "a", "b"]


def test_13_no_numeric_columns_gives_an_empty_list():
    assert numeric_columns(pd.DataFrame({"c": ["x"]})) == []


# ---- 14-17: with_value_where ----


def test_14_sets_the_value_where_the_mask_is_true():
    df = _frame()
    out = with_value_where(df, df["temp"] > 35, "ok", False)
    assert out["ok"].tolist() == [True, False, True, False, True]
    out2 = with_value_where(df, df["temp"] < 31, "city", "COOL")
    assert out2["city"].tolist() == ["Pune", "Delhi", "COOL", "Agra", "COOL"]


def test_15_does_not_change_the_input_frame():
    df = _frame()
    before = df.copy()
    with_value_where(df, df["temp"] > 0, "temp", 0)
    pd.testing.assert_frame_equal(df, before)


def test_16_keeps_index_and_other_columns():
    df = _frame()
    out = with_value_where(df, df["ok"], "temp", -1)
    assert out.index.tolist() == df.index.tolist()
    assert out["city"].tolist() == df["city"].tolist()
    assert out["temp"].tolist() == [-1, 38, -1, 40, -1]


def test_17_all_false_mask_changes_nothing_and_returns_a_separate_frame():
    df = _frame()
    out = with_value_where(df, df["temp"] > 1000, "temp", 0)
    pd.testing.assert_frame_equal(out, df)
    assert out is not df
