"""
pytest data/app_data/99-potd/01-daily/28-cart-category-encoder/tests.py
"""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[3]))
from _load import load_solution  # noqa: E402

_module = load_solution(f"99-potd/01-daily/{Path(__file__).resolve().parent.name}")
encode_departments = _module.encode_departments


def test_example_matches_the_specs_worked_layout():
    distinct, rows = encode_departments(["dairy", "produce", "dairy", "bakery"])
    assert distinct == ["bakery", "dairy", "produce"]
    assert rows == [
        [0, 1, 0],
        [0, 0, 1],
        [0, 1, 0],
        [1, 0, 0],
    ]


def test_single_distinct_department_gives_k_equals_one():
    distinct, rows = encode_departments(["dairy", "dairy", "dairy"])
    assert distinct == ["dairy"]
    assert rows == [[1], [1], [1]]


def test_every_row_a_distinct_department_gives_k_equals_n():
    depts = [f"dept_{i}" for i in range(50)]
    distinct, rows = encode_departments(depts)
    assert len(distinct) == 50
    for i, row in enumerate(rows):
        assert sum(row) == 1
        assert row[distinct.index(depts[i])] == 1


def test_shared_prefixes_are_treated_as_distinct_categories():
    distinct, rows = encode_departments(["dairy", "dairy_alt"])
    assert distinct == ["dairy", "dairy_alt"]
    assert rows[0] != rows[1]
    assert sum(rows[0]) == 1
    assert sum(rows[1]) == 1
