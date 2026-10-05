"""
pytest tests.py
"""

import numpy as np
import pandas as pd
import pytest

from _load import load_solution

_module = load_solution(__file__)
orders_with_customers = _module.orders_with_customers
customer_totals = _module.customer_totals
customers_without_orders = _module.customers_without_orders
safe_merge = _module.safe_merge


def _customers():
    return pd.DataFrame(
        {"id": [3, 1, 2, 4], "name": ["Cara", "Asha", "Ben", "Dev"], "city": ["Goa", "Pune", "Delhi", "Agra"]}
    )


def _orders():
    return pd.DataFrame(
        {
            "order_id": [105, 101, 102, 103, 104],
            "customer_id": [1, 1, 3, 9, 3],
            "amount": [20.0, 10.0, 5.0, 99.0, 7.5],
        }
    )


# ---- 1-5: orders_with_customers ----


def test_1_columns_and_fresh_index():
    out = orders_with_customers(_customers(), _orders())
    assert out.columns.tolist() == ["order_id", "customer_id", "name", "amount"]
    assert out.index.tolist() == list(range(len(out)))


def test_2_sorted_by_order_id_and_values_are_matched():
    out = orders_with_customers(_customers(), _orders())
    assert out["order_id"].tolist() == [101, 102, 104, 105]
    assert out["name"].tolist() == ["Asha", "Cara", "Cara", "Asha"]
    assert out["amount"].tolist() == [10.0, 5.0, 7.5, 20.0]


def test_3_an_order_with_an_unknown_customer_is_dropped():
    out = orders_with_customers(_customers(), _orders())
    assert 103 not in out["order_id"].tolist()


def test_4_a_customer_with_no_orders_does_not_appear():
    out = orders_with_customers(_customers(), _orders())
    assert "Dev" not in out["name"].tolist() and "Ben" not in out["name"].tolist()


def test_5_inputs_are_not_changed():
    c, o = _customers(), _orders()
    cb, ob = c.copy(), o.copy()
    orders_with_customers(c, o)
    pd.testing.assert_frame_equal(c, cb)
    pd.testing.assert_frame_equal(o, ob)


# ---- 6-10: customer_totals ----


def test_6_one_row_per_customer_sorted_by_id():
    out = customer_totals(_customers(), _orders())
    assert out["id"].tolist() == [1, 2, 3, 4]
    assert out.columns.tolist() == ["id", "name", "n_orders", "total"]
    assert out.index.tolist() == [0, 1, 2, 3]


def test_7_counts_and_totals_are_correct():
    out = customer_totals(_customers(), _orders())
    assert out["n_orders"].tolist() == [2, 0, 2, 0]
    assert out["total"].tolist() == [30.0, 0.0, 12.5, 0.0]


def test_8_the_count_stays_an_integer_column():
    out = customer_totals(_customers(), _orders())
    assert out["n_orders"].dtype.kind == "i"
    assert out["total"].dtype.kind == "f"


def test_9_the_orphan_order_is_not_counted_anywhere():
    out = customer_totals(_customers(), _orders())
    assert out["total"].sum() == pytest.approx(42.5)


def test_10_matches_a_python_reference_on_random_data():
    rng = np.random.default_rng(3)
    customers = pd.DataFrame({"id": np.arange(12), "name": [f"c{i}" for i in range(12)], "city": ["x"] * 12})
    orders = pd.DataFrame(
        {"order_id": np.arange(40), "customer_id": rng.integers(0, 16, size=40), "amount": rng.integers(1, 50, size=40).astype(float)}
    )
    out = customer_totals(customers, orders)
    for _, row in out.iterrows():
        mine = orders[orders["customer_id"] == row["id"]]
        assert row["n_orders"] == len(mine)
        assert row["total"] == pytest.approx(mine["amount"].sum())


# ---- 11-13: customers_without_orders ----


def test_11_returns_the_customers_that_never_ordered():
    out = customers_without_orders(_customers(), _orders())
    assert out["name"].tolist() == ["Ben", "Dev"]


def test_12_keeps_all_columns_original_order_and_a_fresh_index():
    out = customers_without_orders(_customers(), _orders())
    assert out.columns.tolist() == ["id", "name", "city"]
    assert out.index.tolist() == [0, 1]
    assert out["id"].tolist() == [2, 4]


def test_13_an_unknown_customer_id_in_orders_does_not_matter():
    orders = pd.DataFrame({"order_id": [1], "customer_id": [999], "amount": [1.0]})
    assert len(customers_without_orders(_customers(), orders)) == 4


# ---- 14-17: safe_merge ----


def test_14_left_join_keeps_every_left_row_in_order():
    left = pd.DataFrame({"k": [3, 1, 2, 1], "x": list("abcd")})
    right = pd.DataFrame({"k": [1, 2], "y": [10, 20]})
    out = safe_merge(left, right, "k")
    assert out["x"].tolist() == list("abcd")
    assert np.isnan(out["y"].iloc[0])
    assert out["y"].iloc[1] == 10 and out["y"].iloc[2] == 20 and out["y"].iloc[3] == 10


def test_15_result_has_a_fresh_index_and_both_sides_columns():
    left = pd.DataFrame({"k": [1, 2], "x": ["a", "b"]}, index=[50, 60])
    right = pd.DataFrame({"k": [1, 2], "y": [1.0, 2.0]})
    out = safe_merge(left, right, "k")
    assert out.index.tolist() == [0, 1]
    assert out.columns.tolist() == ["k", "x", "y"]


def test_16_duplicate_keys_on_the_right_raise_value_error():
    left = pd.DataFrame({"k": [1, 2], "x": ["a", "b"]})
    right = pd.DataFrame({"k": [1, 1, 2], "y": [1, 2, 3]})
    with pytest.raises(ValueError):
        safe_merge(left, right, "k")


def test_17_duplicate_keys_on_the_left_are_fine():
    left = pd.DataFrame({"k": [1, 1, 2], "x": list("abc")})
    right = pd.DataFrame({"k": [1, 2], "y": [7, 8]})
    out = safe_merge(left, right, "k")
    assert out["y"].tolist() == [7, 7, 8]
