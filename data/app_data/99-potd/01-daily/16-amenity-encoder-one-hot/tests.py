"""
pytest data/app_data/99-potd/01-daily/16-amenity-encoder-one-hot/tests.py
"""

import random
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[3]))
from _load import load_solution  # noqa: E402

_module = load_solution(f"99-potd/01-daily/{Path(__file__).resolve().parent.name}")
one_hot_encode = _module.one_hot_encode


def test_example_matches_the_specs_worked_layout():
    distinct, rows = one_hot_encode(["wifi", "parking", "wifi", "pool", "parking"])
    assert distinct == ["parking", "pool", "wifi"]
    assert rows == [
        [0, 0, 1],
        [1, 0, 0],
        [0, 0, 1],
        [0, 1, 0],
        [1, 0, 0],
    ]


def test_single_category_present_gives_all_ones():
    distinct, rows = one_hot_encode(["a", "a", "a"])
    assert distinct == ["a"]
    assert rows == [[1], [1], [1]]


def test_case_sensitivity_treats_different_case_as_distinct():
    distinct, rows = one_hot_encode(["Wifi", "wifi"])
    assert distinct == sorted({"Wifi", "wifi"})
    assert len(distinct) == 2
    assert rows[0] != rows[1]


def test_column_order_is_alphabetical_not_first_appearance():
    distinct, _ = one_hot_encode(["zebra", "apple", "mango"])
    assert distinct == ["apple", "mango", "zebra"]


def test_each_row_has_exactly_one_hot_entry():
    rng = random.Random(11)
    cats = [rng.choice(["red", "green", "blue", "yellow"]) for _ in range(200)]
    distinct, rows = one_hot_encode(cats)
    for row, cat in zip(rows, cats):
        assert sum(row) == 1
        assert row[distinct.index(cat)] == 1


def test_high_cardinality_every_row_distinct():
    n = 2000
    cats = [f"cat_{i}" for i in range(n)]
    distinct, rows = one_hot_encode(cats)
    assert len(distinct) == n
    assert distinct == sorted(cats)
    for i, row in enumerate(rows):
        assert sum(row) == 1
        assert row[distinct.index(cats[i])] == 1
