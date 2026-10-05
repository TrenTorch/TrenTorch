"""
pytest tests.py
"""

import datetime as dt
import math

import numpy as np
import pandas as pd
import pytest

from _load import load_solution

_module = load_solution(__file__)
parse_dates = _module.parse_dates
calendar_features = _module.calendar_features
monthly_total = _module.monthly_total
rolling_average = _module.rolling_average
days_between = _module.days_between


# ---- 1-4: parse_dates ----


def test_1_parses_valid_dates():
    out = parse_dates(pd.Series(["2024-03-07", "2023-12-31"]))
    assert pd.api.types.is_datetime64_any_dtype(out)
    assert out.iloc[0] == pd.Timestamp(2024, 3, 7)
    assert out.iloc[1] == pd.Timestamp(2023, 12, 31)


def test_2_invalid_text_becomes_nat_instead_of_raising():
    out = parse_dates(pd.Series(["2024-03-07", "hello", "2024-02-30", "07/03/2024"]))
    assert out.isna().tolist() == [False, True, True, True]


def test_3_missing_values_become_nat_and_the_index_is_kept():
    s = pd.Series(["2024-01-01", None], index=["a", "b"])
    out = parse_dates(s)
    assert out.index.tolist() == ["a", "b"]
    assert out.isna().tolist() == [False, True]


def test_4_a_leap_day_is_valid_only_in_a_leap_year():
    out = parse_dates(pd.Series(["2024-02-29", "2023-02-29"]))
    assert out.isna().tolist() == [False, True]


# ---- 5-8: calendar_features ----


def test_5_columns_and_index():
    dates = pd.Series(pd.to_datetime(["2024-03-07", "2024-03-09"]), index=["x", "y"])
    out = calendar_features(dates)
    assert out.columns.tolist() == ["year", "month", "dayofweek", "is_weekend"]
    assert out.index.tolist() == ["x", "y"]


def test_6_year_month_and_weekday_values():
    dates = pd.Series(pd.to_datetime(["2024-03-07", "2023-12-31"]))  # Thursday, Sunday
    out = calendar_features(dates)
    assert out["year"].tolist() == [2024, 2023]
    assert out["month"].tolist() == [3, 12]
    assert out["dayofweek"].tolist() == [3, 6]


def test_7_weekend_flag_covers_saturday_and_sunday_only():
    dates = pd.Series(pd.date_range("2024-03-04", periods=7))  # Monday ... Sunday
    assert calendar_features(dates)["is_weekend"].tolist() == [False] * 5 + [True, True]


def test_8_matches_python_datetime_for_a_whole_year():
    dates = pd.Series(pd.date_range("2024-01-01", "2024-12-31"))
    out = calendar_features(dates)
    for ts, row in zip(dates, out.itertuples()):
        py = ts.to_pydatetime().date()
        assert (row.year, row.month, row.dayofweek) == (py.year, py.month, py.weekday())


# ---- 9-12: monthly_total ----


def _orders():
    return pd.DataFrame(
        {
            "when": pd.to_datetime(["2024-01-15", "2024-01-31", "2024-03-01", "2024-03-20", "2024-05-02"]),
            "amount": [10, 5, 7, 3, 20],
        }
    )


def test_9_one_total_per_month_labelled_by_the_first_day():
    out = monthly_total(_orders(), "when", "amount")
    assert out.index[0] == pd.Timestamp(2024, 1, 1)
    assert out.loc[pd.Timestamp(2024, 1, 1)] == 15
    assert out.loc[pd.Timestamp(2024, 3, 1)] == 10


def test_10_empty_months_are_included_with_zero():
    out = monthly_total(_orders(), "when", "amount")
    assert out.index.tolist() == [pd.Timestamp(2024, m, 1) for m in range(1, 6)]
    assert out.loc[pd.Timestamp(2024, 2, 1)] == 0
    assert out.loc[pd.Timestamp(2024, 4, 1)] == 0


def test_11_name_and_grand_total():
    out = monthly_total(_orders(), "when", "amount")
    assert out.name == "amount"
    assert out.sum() == 45


def test_12_matches_a_python_reference_on_random_data():
    rng = np.random.default_rng(5)
    days = pd.Timestamp("2023-06-01") + pd.to_timedelta(rng.integers(0, 400, size=80), unit="D")
    df = pd.DataFrame({"d": days, "v": rng.integers(1, 30, size=80)})
    out = monthly_total(df, "d", "v")
    for month_start, total in out.items():
        expected = sum(v for d, v in zip(df["d"], df["v"]) if (d.year, d.month) == (month_start.year, month_start.month))
        assert total == expected


# ---- 13-15: rolling_average ----


def test_13_first_window_minus_one_values_are_nan():
    s = pd.Series([1.0, 2.0, 3.0, 4.0, 5.0], index=pd.date_range("2024-01-01", periods=5))
    out = rolling_average(s, 3)
    assert out.isna().tolist() == [True, True, False, False, False]


def test_14_values_are_window_means():
    s = pd.Series([1.0, 2.0, 3.0, 4.0, 5.0], index=pd.date_range("2024-01-01", periods=5))
    out = rolling_average(s, 3)
    assert out.iloc[2:].tolist() == [2.0, 3.0, 4.0]


def test_15_window_one_returns_the_series_and_the_index_is_kept():
    s = pd.Series([4.0, 8.0], index=pd.date_range("2024-02-01", periods=2))
    out = rolling_average(s, 1)
    assert out.tolist() == [4.0, 8.0]
    assert out.index.equals(s.index)


# ---- 16-18: days_between ----


def test_16_whole_days_between_dates():
    a = pd.Series(pd.to_datetime(["2024-01-01", "2024-02-28"]))
    b = pd.Series(pd.to_datetime(["2024-01-31", "2024-03-01"]))
    assert days_between(a, b).tolist() == [30, 2]  # 2024 is a leap year


def test_17_negative_when_end_is_earlier_and_zero_for_the_same_day():
    a = pd.Series(pd.to_datetime(["2024-05-10", "2024-05-10"]))
    b = pd.Series(pd.to_datetime(["2024-05-01", "2024-05-10"]))
    assert days_between(a, b).tolist() == [-9, 0]


def test_18_integer_result_with_the_inputs_index():
    a = pd.Series(pd.to_datetime(["2024-01-01"]), index=["k"])
    b = pd.Series(pd.to_datetime(["2024-01-11"]), index=["k"])
    out = days_between(a, b)
    assert out.index.tolist() == ["k"]
    assert out.dtype.kind == "i"
