"""
pytest data/app_data/00-python/05-dictionaries/08-assemble-summarize-orders/tests.py
"""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[3]))
from _load import load_solution  # noqa: E402

_module = load_solution(f"00-python/05-dictionaries/{Path(__file__).resolve().parent.name}")
summarize_orders = _module.summarize_orders

ORDERS = [
    {"customer": "Bob", "items": {"sku1": 2, "sku2": 3}},
    {"customer": "Alice", "items": {"sku1": 5}},
    {"customer": "Bob", "items": {"sku2": 1}},
    {"customer": "annie", "items": {}},
]


def test_totals_across_repeated_customers_and_skus():
    result = summarize_orders(ORDERS)
    assert result["units_by_customer"]["Bob"] == 6
    assert result["units_by_sku"]["sku2"] == 4


def test_customers_with_empty_orders():
    result = summarize_orders(ORDERS)
    assert result["units_by_customer"]["annie"] == 0
    for skus in result["customers_by_sku"].values():
        assert "annie" not in skus


def test_top_sku_tie_break_and_empty_case():
    orders = [
        {"customer": "a", "items": {"z": 5, "a": 5}},
    ]
    result = summarize_orders(orders)
    assert result["top_sku"] == "a"
    assert summarize_orders([])["top_sku"] is None


def test_customers_by_sku_distinct_and_sorted():
    orders = [
        {"customer": "Bob", "items": {"sku1": 1}},
        {"customer": "Bob", "items": {"sku1": 2}},
        {"customer": "Alice", "items": {"sku1": 1}},
    ]
    result = summarize_orders(orders)
    assert result["customers_by_sku"]["sku1"] == ["Alice", "Bob"]


def test_customers_by_initial_case_handling():
    result = summarize_orders(ORDERS)
    assert result["customers_by_initial"]["A"] == ["Alice", "annie"]
    assert result["customers_by_initial"]["B"] == ["Bob"]
    assert "" not in result["customers_by_initial"]


def test_input_immutability():
    import copy

    snapshot = copy.deepcopy(ORDERS)
    summarize_orders(ORDERS)
    assert ORDERS == snapshot


def test_no_shared_list_objects_in_result():
    orders = [
        {"customer": "Bob", "items": {"sku1": 1, "sku2": 1}},
    ]
    result = summarize_orders(orders)
    lists = list(result["customers_by_sku"].values()) + list(
        result["customers_by_initial"].values()
    )
    ids = [id(lst) for lst in lists]
    assert len(ids) == len(set(ids))
