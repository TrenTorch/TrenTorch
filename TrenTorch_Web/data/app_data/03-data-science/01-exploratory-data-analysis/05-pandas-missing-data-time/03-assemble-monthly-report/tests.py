"""
pytest tests.py
"""

import math
from collections import defaultdict
from datetime import date

import numpy as np
import pandas as pd
import pytest

from _load import load_solution

_module = load_solution(__file__)
monthly_report = _module.monthly_report


def _customers():
    return pd.DataFrame({"id": [1, 2, 3], "region": ["west", "east", "west"]})


def _orders():
    return pd.DataFrame(
        {
            "order_id": range(1, 10),
            "customer_id": [1, 2, 3, 2, 1, 9, 2, 1, 3],
            "order_date": ["2024-01-05", "2024-01-20", "2024-01-31", "2024-03-02", "2024-03-15", "2024-03-16", "not a date", "2024-04-01", "2024-04-30"],
            "amount": [10.0, 30.0, 10.0, 40.0, 20.0, 999.0, 500.0, 5.0, 15.0],
        }
    )


def _isnull(x):
    return x is None or (isinstance(x, float) and math.isnan(x))


def _reference(orders, customers):
    region_of = dict(zip(customers["id"], customers["region"]))
    months = {}
    for _, row in orders.iterrows():
        try:
            d = date.fromisoformat(row["order_date"])
        except (ValueError, TypeError):
            continue
        if row["customer_id"] not in region_of:
            continue
        months.setdefault((d.year, d.month), []).append((region_of[row["customer_id"]], float(row["amount"])))
    if not months:
        return []
    first, last = min(months), max(months)
    out, y, m, prev = [], first[0], first[1], None
    while (y, m) <= last:
        rows = months.get((y, m), [])
        revenue = sum(a for _, a in rows)
        by_region = defaultdict(float)
        for r, a in rows:
            by_region[r] += a
        top = None
        if by_region:
            top = sorted(by_region.items(), key=lambda kv: (-kv[1], kv[0]))[0][0]
        growth = math.nan if prev is None or prev <= 0 else 100.0 * (revenue - prev) / prev
        out.append((pd.Timestamp(y, m, 1), len(rows), revenue, revenue / len(rows) if rows else math.nan, growth, top))
        prev = revenue
        y, m = (y + 1, 1) if m == 12 else (y, m + 1)
    return out


# ---- 1-4: shape ----


def test_1_index_is_month_start_named_month_and_covers_the_calendar():
    out = monthly_report(_orders(), _customers())
    assert out.index.name == "month"
    assert out.index.tolist() == [pd.Timestamp(2024, m, 1) for m in (1, 2, 3, 4)]


def test_2_columns_in_order():
    out = monthly_report(_orders(), _customers())
    assert out.columns.tolist() == ["orders", "revenue", "avg_order_value", "growth_pct", "top_region"]


def test_3_orders_is_an_integer_column_and_revenue_a_float_column():
    out = monthly_report(_orders(), _customers())
    assert out["orders"].dtype.kind == "i"
    assert out["revenue"].dtype.kind == "f"


def test_4_inputs_are_not_changed():
    o, c = _orders(), _customers()
    ob, cb = o.copy(), c.copy()
    monthly_report(o, c)
    pd.testing.assert_frame_equal(o, ob)
    pd.testing.assert_frame_equal(c, cb)


# ---- 5-9: the numbers ----


def test_5_counts_and_revenue_ignore_bad_dates_and_unknown_customers():
    out = monthly_report(_orders(), _customers())
    assert out["orders"].tolist() == [3, 0, 2, 2]
    assert out["revenue"].tolist() == [50.0, 0.0, 60.0, 20.0]


def test_6_average_order_value_is_nan_for_an_empty_month():
    out = monthly_report(_orders(), _customers())
    assert out["avg_order_value"].iloc[0] == pytest.approx(50 / 3)
    assert math.isnan(out["avg_order_value"].iloc[1])
    assert out["avg_order_value"].iloc[2] == pytest.approx(30.0)


def test_7_growth_is_nan_for_the_first_month_and_after_a_zero_month():
    out = monthly_report(_orders(), _customers())
    g = out["growth_pct"].tolist()
    assert math.isnan(g[0])
    assert g[1] == pytest.approx(-100.0)
    assert math.isnan(g[2])  # previous month revenue is 0
    assert g[3] == pytest.approx(100 * (20 - 60) / 60)


def test_8_top_region_picks_the_biggest_with_ties_going_to_the_smaller_name():
    out = monthly_report(_orders(), _customers())
    # Jan: east 30, west 10 + 10 = 20 -> east. Mar: east 40, west 20 -> east.
    assert out["top_region"].iloc[0] == "east"
    assert _isnull(out["top_region"].iloc[1])
    assert out["top_region"].iloc[2] == "east"
    # Apr: west 5 + 15 = 20 only.
    assert out["top_region"].iloc[3] == "west"
    tie = pd.DataFrame({"order_id": [1, 2], "customer_id": [1, 2], "order_date": ["2024-01-01", "2024-01-02"], "amount": [10.0, 10.0]})
    assert monthly_report(tie, _customers())["top_region"].iloc[0] == "east"


def test_9_revenue_reconciles_with_the_valid_input_rows():
    out = monthly_report(_orders(), _customers())
    assert out["revenue"].sum() == pytest.approx(130.0)
    assert out["orders"].sum() == 7


# ---- 10-12: edge cases ----


def test_10_no_valid_orders_gives_an_empty_frame_with_the_columns():
    bad = pd.DataFrame({"order_id": [1], "customer_id": [1], "order_date": ["nope"], "amount": [1.0]})
    out = monthly_report(bad, _customers())
    assert out.empty
    assert out.columns.tolist() == ["orders", "revenue", "avg_order_value", "growth_pct", "top_region"]


def test_11_a_single_month():
    one = pd.DataFrame({"order_id": [1, 2], "customer_id": [1, 3], "order_date": ["2024-06-01", "2024-06-30"], "amount": [4.0, 6.0]})
    out = monthly_report(one, _customers())
    assert len(out) == 1
    assert out["orders"].iloc[0] == 2 and out["revenue"].iloc[0] == 10.0
    assert math.isnan(out["growth_pct"].iloc[0])


def test_12_crosses_a_year_boundary():
    two = pd.DataFrame({"order_id": [1, 2], "customer_id": [1, 1], "order_date": ["2023-11-10", "2024-02-10"], "amount": [10.0, 20.0]})
    out = monthly_report(two, _customers())
    assert out.index.tolist() == [pd.Timestamp(2023, 11, 1), pd.Timestamp(2023, 12, 1), pd.Timestamp(2024, 1, 1), pd.Timestamp(2024, 2, 1)]
    assert out["orders"].tolist() == [1, 0, 0, 1]


# ---- 13-14: reference comparison ----


def test_13_matches_a_plain_python_reference_on_random_data():
    for seed in range(5):
        rng = np.random.default_rng(seed)
        n = 60
        days = pd.Timestamp("2023-09-01") + pd.to_timedelta(rng.integers(0, 330, size=n), unit="D")
        text = [d.strftime("%Y-%m-%d") for d in days]
        for i in rng.choice(n, size=4, replace=False):
            text[i] = "bad"
        orders = pd.DataFrame(
            {"order_id": range(n), "customer_id": rng.integers(0, 6, size=n), "order_date": text, "amount": rng.integers(1, 40, size=n).astype(float)}
        )
        customers = pd.DataFrame({"id": [0, 1, 2, 3, 4], "region": ["n", "s", "e", "w", "s"]})
        out = monthly_report(orders, customers)
        ref = _reference(orders, customers)
        assert len(out) == len(ref)
        for (ts, count, revenue, avg, growth, top), (idx, row) in zip(ref, out.iterrows()):
            assert idx == ts
            assert row["orders"] == count
            assert row["revenue"] == pytest.approx(revenue)
            assert (_isnull(avg) and _isnull(row["avg_order_value"])) or row["avg_order_value"] == pytest.approx(avg)
            assert (_isnull(growth) and _isnull(row["growth_pct"])) or row["growth_pct"] == pytest.approx(growth)
            assert (top is None and _isnull(row["top_region"])) or row["top_region"] == top


def test_14_an_unknown_customer_id_is_ignored_even_when_it_is_the_only_order_in_a_month():
    orders = pd.DataFrame({"order_id": [1, 2], "customer_id": [1, 77], "order_date": ["2024-01-02", "2024-02-02"], "amount": [5.0, 9.0]})
    out = monthly_report(orders, _customers())
    assert out.index.tolist() == [pd.Timestamp(2024, 1, 1)]
