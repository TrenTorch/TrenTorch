"""
pytest tests.py
"""

from _load import load_solution

_module = load_solution(__file__)
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
