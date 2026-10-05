"""
pytest tests.py
"""

import math
import statistics

import numpy as np
import pandas as pd
import pytest

from _load import load_solution

_module = load_solution(__file__)
missing_report = _module.missing_report
fill_group_median = _module.fill_group_median
forward_fill_limit = _module.forward_fill_limit
drop_sparse_columns = _module.drop_sparse_columns
fill_with_indicator = _module.fill_with_indicator


def _isnan(x):
    return x is None or (isinstance(x, float) and math.isnan(x))


def _df():
    return pd.DataFrame(
        {
            "city": ["a", "a", "b", "b", "c", None, "a", "b"],
            "income": [10.0, np.nan, 30.0, 50.0, np.nan, 40.0, 20.0, np.nan],
            "age": [25, 30, np.nan, 41, 52, 19, 33, 28],
            "note": [np.nan] * 6 + ["x", np.nan],
        }
    )


# ---- 1-4: missing_report ----


def test_1_only_columns_with_holes_appear():
    out = missing_report(_df())
    assert set(out.index) == {"city", "income", "age", "note"}
    full = pd.DataFrame({"a": [1, 2], "b": [1.0, np.nan]})
    assert missing_report(full).index.tolist() == ["b"]


def test_2_counts_and_percentages():
    out = missing_report(_df())
    assert out.loc["income", "n_missing"] == 3
    assert out.loc["note", "n_missing"] == 7
    assert out.loc["income", "pct"] == 37.5
    assert out.loc["note", "pct"] == 87.5


def test_3_ordered_by_count_then_name():
    out = missing_report(_df())
    assert out.index.tolist() == ["note", "income", "age", "city"]
    tie = pd.DataFrame({"z": [np.nan, 1.0], "a": [np.nan, 2.0]})
    assert missing_report(tie).index.tolist() == ["a", "z"]


def test_4_nothing_missing_gives_an_empty_frame_with_the_two_columns():
    out = missing_report(pd.DataFrame({"a": [1, 2]}))
    assert out.empty
    assert out.columns.tolist() == ["n_missing", "pct"]


# ---- 5-9: fill_group_median ----


def test_5_fills_with_the_group_median():
    out = fill_group_median(_df(), "city", "income")
    assert out.iloc[1] == pytest.approx(15.0)  # city a: known 10, 20
    assert out.iloc[7] == pytest.approx(40.0)  # city b: known 30, 50


def test_6_known_values_are_unchanged():
    df = _df()
    out = fill_group_median(df, "city", "income")
    known = df["income"].notna()
    assert out[known].tolist() == df["income"][known].tolist()


def test_7_a_group_with_no_known_value_uses_the_overall_median():
    out = fill_group_median(_df(), "city", "income")
    overall = statistics.median([10.0, 30.0, 50.0, 40.0, 20.0])
    assert out.iloc[4] == pytest.approx(overall)  # city c has only a missing income


def test_8_a_missing_key_uses_the_overall_median():
    df = pd.DataFrame({"k": ["a", None, "a"], "v": [1.0, np.nan, 3.0]})
    assert fill_group_median(df, "k", "v").iloc[1] == pytest.approx(2.0)


def test_9_keeps_the_index_returns_floats_and_leaves_the_input_alone():
    df = _df()
    df.index = list("pqrstuvw")
    before = df.copy()
    out = fill_group_median(df, "city", "income")
    assert out.index.tolist() == list("pqrstuvw")
    assert out.dtype.kind == "f"
    pd.testing.assert_frame_equal(df, before)


# ---- 10-12: forward_fill_limit ----


def test_10_carries_the_last_value_forward():
    s = pd.Series([1.0, np.nan, np.nan, 4.0, np.nan])
    assert forward_fill_limit(s, 5).tolist() == [1.0, 1.0, 1.0, 4.0, 4.0]


def test_11_stops_after_limit_consecutive_fills():
    s = pd.Series([1.0, np.nan, np.nan, np.nan, 5.0])
    out = forward_fill_limit(s, 2).tolist()
    assert out[:3] == [1.0, 1.0, 1.0] and math.isnan(out[3]) and out[4] == 5.0


def test_12_leading_missing_values_stay_missing():
    out = forward_fill_limit(pd.Series([np.nan, np.nan, 3.0]), 3).tolist()
    assert math.isnan(out[0]) and math.isnan(out[1]) and out[2] == 3.0


# ---- 13-15: drop_sparse_columns ----


def test_13_drops_columns_missing_more_than_the_threshold():
    out = drop_sparse_columns(_df(), 0.5)
    assert out.columns.tolist() == ["city", "income", "age"]


def test_14_a_column_exactly_at_the_threshold_is_kept():
    out = drop_sparse_columns(_df(), 0.375)
    assert "income" in out.columns and "note" not in out.columns


def test_15_zero_threshold_keeps_only_complete_columns_and_the_original_order():
    df = pd.DataFrame({"b": [1, 2], "a": [1.0, np.nan], "c": [3, 4]})
    assert drop_sparse_columns(df, 0.0).columns.tolist() == ["b", "c"]


# ---- 16-18: fill_with_indicator ----


def test_16_fills_with_the_median_and_adds_the_indicator_last():
    out = fill_with_indicator(_df(), "income")
    assert out.columns.tolist()[-1] == "income_was_missing"
    assert out["income"].tolist() == [10.0, 30.0, 30.0, 50.0, 30.0, 40.0, 20.0, 30.0]
    assert out["income_was_missing"].tolist() == [False, True, False, False, True, False, False, True]


def test_17_indicator_is_boolean_and_other_columns_are_untouched():
    df = _df()
    out = fill_with_indicator(df, "age")
    assert out["age_was_missing"].dtype == bool
    assert out["note"].isna().sum() == df["note"].isna().sum()
    assert out["city"].tolist()[:5] == df["city"].tolist()[:5]


def test_18_the_input_is_not_changed():
    df = _df()
    before = df.copy()
    fill_with_indicator(df, "income")
    pd.testing.assert_frame_equal(df, before)
