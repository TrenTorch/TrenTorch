"""
pytest data/app_data/00-python/03-lists/09-assemble-inventory-cleanup/tests.py
"""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[3]))
from _load import load_solution  # noqa: E402

_module = load_solution(f"00-python/03-lists/{Path(__file__).resolve().parent.name}")
process_inventory = _module.process_inventory


def test_rows_below_threshold_removed_in_place():
    rows = [["a", 1], ["b", 1], ["c", 10]]
    before_id = id(rows)
    process_inventory(rows, 5)
    assert id(rows) == before_id
    assert [r[0] for r in rows] == ["c"]


def test_surviving_rows_are_the_original_objects():
    row_a = ["a", 10]
    row_b = ["b", 1]
    rows = [row_a, row_b]
    process_inventory(rows, 5)
    assert rows[0] is row_a


def test_sort_order_with_ties():
    rows = [["b", 5], ["a", 5], ["c", 10]]
    process_inventory(rows, 0)
    assert [r[0] for r in rows] == ["c", "a", "b"]
    assert [r[1] for r in rows] == [10, 5, 5]


def test_snapshot_is_independent():
    rows = [["a", 1], ["b", 10]]
    result = process_inventory(rows, 5)
    snapshot = result[0]
    assert snapshot == [["a", 1], ["b", 10]]
    assert id(snapshot[0]) != id(rows[0]) if rows else True
    rows.append(["c", 99])
    assert snapshot == [["a", 1], ["b", 10]]


def test_top_labels_slice_bounds():
    rows = [["a", 1]]
    result = process_inventory(rows, 0)
    assert result[1] == ["a"]

    rows2 = [["a", 4], ["b", 3], ["c", 2], ["d", 1]]
    result2 = process_inventory(rows2, 0)
    assert result2[1] == ["a", "b", "c"]

    rows3 = [["a", 1]]
    result3 = process_inventory(rows3, 5)
    assert result3[1] == []


def test_quantities_matches_sorted_order():
    rows = [["a", 1], ["b", 3], ["c", 2]]
    result = process_inventory(rows, 0)
    assert result[2] == [3, 2, 1]


def test_return_structure_and_empty_input():
    rows = []
    result = process_inventory(rows, 0)
    assert result == [[], [], []]
    assert rows == []
