"""
pytest tests.py
"""

import random

import pytest

from _load import load_solution

_module = load_solution(__file__)
group_by = _module.group_by
having = _module.having
count_distinct = _module.count_distinct

ORDERS = [
    {"country": "IN", "plan": "pro", "amount": 10.0},
    {"country": "IN", "plan": "free", "amount": 0.0},
    {"country": "US", "plan": "pro", "amount": 30.0},
    {"country": "IN", "plan": "pro", "amount": 20.0},
    {"country": "US", "plan": "free", "amount": None},
]


# ---- 1-9: grouping ----


def test_1_hand_computed_sum_count_mean():
    out = group_by(
        ORDERS,
        ["country"],
        {"n": ("amount", "count"), "total": ("amount", "sum"), "avg": ("amount", "mean")},
    )
    assert out == [
        {"country": "IN", "n": 3, "total": 30.0, "avg": 10.0},
        {"country": "US", "n": 2, "total": 30.0, "avg": 30.0},
    ]


def test_2_min_and_max():
    out = group_by(ORDERS, ["country"], {"lo": ("amount", "min"), "hi": ("amount", "max")})
    assert out[0] == {"country": "IN", "lo": 0.0, "hi": 20.0}


def test_3_groups_are_sorted_by_the_key_tuple():
    rows = [{"k": "b"}, {"k": "a"}, {"k": "c"}, {"k": "a"}]
    out = group_by(rows, ["k"], {"n": ("k", "count")})
    assert [g["k"] for g in out] == ["a", "b", "c"] and out[0]["n"] == 2


def test_4_several_key_columns():
    out = group_by(ORDERS, ["country", "plan"], {"n": ("amount", "count")})
    assert [(g["country"], g["plan"], g["n"]) for g in out] == [
        ("IN", "free", 1),
        ("IN", "pro", 2),
        ("US", "free", 1),
        ("US", "pro", 1),
    ]


def test_5_output_column_order_is_keys_then_aggregates_as_given():
    out = group_by(ORDERS, ["country"], {"b": ("amount", "sum"), "a": ("amount", "count")})
    assert list(out[0].keys()) == ["country", "b", "a"]


def test_6_nones_are_skipped_but_count_counts_every_row():
    out = group_by(ORDERS, ["country"], {"n": ("amount", "count"), "avg": ("amount", "mean")})
    us = out[1]
    assert us["n"] == 2 and us["avg"] == 30.0


def test_7_all_none_group_gives_none_for_value_aggregates():
    rows = [{"k": 1, "v": None}, {"k": 1, "v": None}]
    out = group_by(rows, ["k"], {"s": ("v", "sum"), "m": ("v", "mean"), "lo": ("v", "min"), "n": ("v", "count")})
    assert out == [{"k": 1, "s": None, "m": None, "lo": None, "n": 2}]


def test_8_empty_table_and_unknown_function():
    assert group_by([], ["k"], {"n": ("k", "count")}) == []
    with pytest.raises(ValueError):
        group_by(ORDERS, ["country"], {"x": ("amount", "median")})


def test_9_matches_a_brute_force_computation():
    rng = random.Random(0)
    rows = [{"g": rng.randint(0, 4), "v": rng.randint(1, 100)} for _ in range(300)]
    out = group_by(rows, ["g"], {"total": ("v", "sum"), "n": ("v", "count")})
    for group in out:
        members = [r["v"] for r in rows if r["g"] == group["g"]]
        assert group["total"] == sum(members) and group["n"] == len(members)


# ---- 10-12: having ----


def test_10_having_filters_on_aggregates():
    out = group_by(ORDERS, ["country"], {"n": ("amount", "count")})
    assert having(out, lambda g: g["n"] >= 3) == [{"country": "IN", "n": 3}]


def test_11_having_keeps_the_order_and_can_keep_everything_or_nothing():
    out = group_by(ORDERS, ["country"], {"n": ("amount", "count")})
    assert having(out, lambda g: True) == out
    assert having(out, lambda g: False) == []


def test_12_having_does_not_modify_the_groups():
    out = group_by(ORDERS, ["country"], {"n": ("amount", "count")})
    snapshot = [dict(g) for g in out]
    having(out, lambda g: g["n"] > 2)
    assert out == snapshot


# ---- 13-15: distinct counts and purity ----


def test_13_count_distinct_ignores_none_and_duplicates():
    rows = [{"u": 1}, {"u": 2}, {"u": 1}, {"u": None}, {"u": 3}]
    assert count_distinct(rows, "u") == 3


def test_14_count_distinct_of_an_empty_table_is_zero():
    assert count_distinct([], "u") == 0


def test_15_input_rows_are_not_modified():
    rows = [dict(r) for r in ORDERS]
    group_by(rows, ["country"], {"total": ("amount", "sum")})
    count_distinct(rows, "plan")
    assert rows == ORDERS
