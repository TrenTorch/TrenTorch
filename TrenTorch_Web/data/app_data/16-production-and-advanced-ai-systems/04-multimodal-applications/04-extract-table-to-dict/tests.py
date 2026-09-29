"""pytest data/app_data/16-production-and-advanced-ai-systems/04-multimodal-applications/04-extract-table-to-dict/tests.py"""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[3]))
from _load import load_solution  # noqa: E402

rows_to_records = load_solution(
    f"16-production-and-advanced-ai-systems/04-multimodal-applications/{Path(__file__).resolve().parent.name}"
).rows_to_records


def test_1_simple_table():
    header = ["name", "quantity"]
    rows = [["apples", "3"], ["bananas", "5"]]
    assert rows_to_records(header, rows) == [
        {"name": "apples", "quantity": "3"},
        {"name": "bananas", "quantity": "5"},
    ]


def test_2_empty_rows_returns_empty_list():
    assert rows_to_records(["a", "b"], []) == []


def test_3_row_shorter_than_header_drops_missing_columns():
    header = ["name", "quantity", "price"]
    rows = [["apples", "3"]]
    assert rows_to_records(header, rows) == [{"name": "apples", "quantity": "3"}]


def test_4_row_longer_than_header_drops_extra_cells():
    header = ["name", "quantity"]
    rows = [["apples", "3", "extra"]]
    assert rows_to_records(header, rows) == [{"name": "apples", "quantity": "3"}]


def test_5_single_column_table():
    assert rows_to_records(["id"], [["1"], ["2"]]) == [{"id": "1"}, {"id": "2"}]
