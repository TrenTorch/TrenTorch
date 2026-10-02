"""
pytest tests.py
"""

import random

import pytest

from _load import load_solution

_module = load_solution(__file__)
rows_to_columns = _module.rows_to_columns
columns_to_rows = _module.columns_to_rows
run_length_encode = _module.run_length_encode
run_length_decode = _module.run_length_decode
bytes_scanned = _module.bytes_scanned

ROWS = [
    {"id": 1, "city": "pune", "age": 30},
    {"id": 2, "city": "pune", "age": 41},
    {"id": 3, "city": "delhi", "age": 25},
]


# ---- 1-6: layouts ----


def test_1_rows_to_columns_hand_computed():
    assert rows_to_columns(ROWS) == {
        "id": [1, 2, 3],
        "city": ["pune", "pune", "delhi"],
        "age": [30, 41, 25],
    }


def test_2_column_order_follows_the_row_keys():
    assert list(rows_to_columns(ROWS)) == ["id", "city", "age"]


def test_3_columns_to_rows_hand_computed():
    columns = {"a": [1, 2], "b": ["x", "y"]}
    assert columns_to_rows(columns) == [{"a": 1, "b": "x"}, {"a": 2, "b": "y"}]


def test_4_round_trip_in_both_directions():
    assert columns_to_rows(rows_to_columns(ROWS)) == ROWS
    columns = {"u": [1, 2, 3], "v": [4, 5, 6]}
    assert rows_to_columns(columns_to_rows(columns)) == columns


def test_5_empty_tables():
    assert rows_to_columns([]) == {} and columns_to_rows({}) == []


def test_6_inputs_are_not_modified():
    rows = [dict(r) for r in ROWS]
    columns = rows_to_columns(rows)
    snapshot = {k: list(v) for k, v in columns.items()}
    columns_to_rows(columns)
    rows_to_columns(rows)
    assert rows == ROWS and columns == snapshot


# ---- 7-12: run-length encoding ----


def test_7_encodes_runs():
    assert run_length_encode(list("AAABBA")) == [("A", 3), ("B", 2), ("A", 1)]


def test_8_a_list_with_no_repeats_has_one_run_per_value():
    assert run_length_encode([1, 2, 3]) == [(1, 1), (2, 1), (3, 1)]


def test_9_empty_and_constant_lists():
    assert run_length_encode([]) == []
    assert run_length_encode([7] * 100) == [(7, 100)]


def test_10_decode_inverts_encode():
    rng = random.Random(0)
    values = [rng.choice("abc") for _ in range(300)]
    assert run_length_decode(run_length_encode(values)) == values


def test_11_decode_hand_computed():
    assert run_length_decode([("x", 2), ("y", 1), ("x", 3)]) == ["x", "x", "y", "x", "x", "x"]


def test_12_sorting_a_column_creates_long_runs_and_shrinks_the_encoding():
    rng = random.Random(1)
    values = [rng.choice(["IN", "US", "UK"]) for _ in range(900)]
    assert len(run_length_encode(sorted(values))) == 3
    assert len(run_length_encode(values)) > 300


# ---- 13-17: scan cost ----


def test_13_row_store_reads_everything():
    assert bytes_scanned("row", 1000, 10, 1, 8) == 80_000


def test_14_column_store_reads_only_the_needed_columns():
    assert bytes_scanned("column", 1000, 10, 1, 8) == 8_000


def test_15_the_saving_is_columns_over_columns_needed():
    row = bytes_scanned("row", 500, 20, 4, 4)
    column = bytes_scanned("column", 500, 20, 4, 4)
    assert row // column == 5


def test_16_reading_every_column_costs_the_same_in_both_layouts():
    assert bytes_scanned("row", 100, 6, 6, 8) == bytes_scanned("column", 100, 6, 6, 8)


def test_17_unknown_layout_raises_value_error():
    with pytest.raises(ValueError):
        bytes_scanned("graph", 1, 1, 1, 1)
