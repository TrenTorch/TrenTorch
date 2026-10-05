"""
pytest tests.py
"""

import math
import statistics
from collections import Counter

import numpy as np
import pandas as pd
import pytest

from _load import load_solution

_module = load_solution(__file__)
profile = _module.profile


def _df():
    return pd.DataFrame(
        {
            "age": [25, 30, 30, np.nan, 41],
            "city": ["Pune", "Delhi", "Delhi", "Pune", None],
            "member": [True, False, True, True, False],
            "score": [1.5, 2.5, 2.5, 4.0, 9.0],
        }
    )


def _isnan(x):
    return isinstance(x, float) and math.isnan(x)


# ---- 1-4: shape, missing, duplicates ----


def test_1_has_exactly_the_documented_keys():
    assert set(profile(_df())) == {"n_rows", "n_cols", "missing", "n_duplicate_rows", "numeric", "categorical"}


def test_2_size_is_reported_as_python_ints():
    out = profile(_df())
    assert out["n_rows"] == 5 and out["n_cols"] == 4
    assert type(out["n_rows"]) is int and type(out["n_cols"]) is int


def test_3_missing_counts_every_column_in_order():
    out = profile(_df())
    assert list(out["missing"]) == ["age", "city", "member", "score"]
    assert out["missing"] == {"age": 1, "city": 1, "member": 0, "score": 0}
    assert all(type(v) is int for v in out["missing"].values())


def test_4_duplicates_do_not_count_the_first_occurrence():
    df = pd.DataFrame({"a": [1, 1, 1, 2], "b": ["x", "x", "x", "y"]})
    assert profile(df)["n_duplicate_rows"] == 2
    assert profile(pd.DataFrame({"a": [1, 2, 3]}))["n_duplicate_rows"] == 0


# ---- 5-9: numeric ----


def test_5_numeric_columns_are_the_int_and_float_ones_only():
    out = profile(_df())
    assert list(out["numeric"]) == ["age", "score"]
    assert "member" not in out["numeric"]


def test_6_summary_values_ignore_missing_and_use_the_sample_std():
    out = profile(_df())["numeric"]["age"]
    values = [25, 30, 30, 41]
    assert out["mean"] == pytest.approx(statistics.mean(values))
    assert out["std"] == pytest.approx(statistics.stdev(values))
    assert out["min"] == 25.0 and out["max"] == 41.0


def test_7_values_are_python_floats():
    for stats in profile(_df())["numeric"].values():
        assert all(type(v) is float for v in stats.values())


def test_8_a_single_value_has_no_std_and_an_empty_column_has_no_stats():
    one = profile(pd.DataFrame({"x": [7.0, np.nan]}))["numeric"]["x"]
    assert one["mean"] == 7.0 and one["min"] == 7.0 and _isnan(one["std"])
    empty = profile(pd.DataFrame({"x": [np.nan, np.nan]}))["numeric"]["x"]
    assert all(_isnan(v) for v in empty.values())


def test_9_matches_a_plain_python_reference_on_random_data():
    rng = np.random.default_rng(4)
    values = rng.normal(10, 3, size=40)
    values[[2, 9]] = np.nan
    stats = profile(pd.DataFrame({"v": values}))["numeric"]["v"]
    known = [v for v in values if not np.isnan(v)]
    assert stats["mean"] == pytest.approx(statistics.mean(known))
    assert stats["std"] == pytest.approx(statistics.stdev(known))
    assert stats["min"] == pytest.approx(min(known)) and stats["max"] == pytest.approx(max(known))


# ---- 10-14: categorical ----


def test_10_booleans_and_text_are_categorical():
    out = profile(_df())["categorical"]
    assert list(out) == ["city", "member"]


def test_11_unique_top_and_count_ignore_missing():
    out = profile(_df())["categorical"]["city"]
    # Delhi and Pune both occur twice; the smaller value wins.
    assert out == {"n_unique": 2, "top": "Delhi", "top_count": 2}


def test_12_ties_resolve_to_the_smallest_value_regardless_of_row_order():
    a = pd.DataFrame({"c": ["b", "a", "b", "a", "c"]})
    b = pd.DataFrame({"c": ["c", "b", "a", "a", "b"]})
    assert profile(a)["categorical"]["c"]["top"] == "a"
    assert profile(b)["categorical"]["c"]["top"] == "a"


def test_13_an_all_missing_categorical_column():
    out = profile(pd.DataFrame({"c": [None, None]}))["categorical"]["c"]
    assert out == {"n_unique": 0, "top": None, "top_count": 0}


def test_14_matches_a_counter_reference():
    rng = np.random.default_rng(1)
    col = rng.choice(["x", "y", "z", "w"], size=60).tolist()
    out = profile(pd.DataFrame({"c": col}))["categorical"]["c"]
    counts = Counter(col)
    best = max(counts.values())
    assert out["n_unique"] == len(counts)
    assert out["top_count"] == best
    assert out["top"] == min(k for k, v in counts.items() if v == best)


# ---- 15-16: whole-frame behaviour ----


def test_15_does_not_change_the_input():
    df = _df()
    before = df.copy()
    profile(df)
    pd.testing.assert_frame_equal(df, before)


def test_16_an_empty_frame_with_columns():
    df = pd.DataFrame({"a": pd.Series([], dtype=float), "b": pd.Series([], dtype=object)})
    out = profile(df)
    assert out["n_rows"] == 0 and out["n_cols"] == 2
    assert out["missing"] == {"a": 0, "b": 0}
    assert out["categorical"]["b"] == {"n_unique": 0, "top": None, "top_count": 0}
