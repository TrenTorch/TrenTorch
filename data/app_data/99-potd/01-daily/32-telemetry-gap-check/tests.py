"""
pytest data/app_data/99-potd/01-daily/32-telemetry-gap-check/tests.py
"""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[3]))
from _load import load_solution  # noqa: E402

_module = load_solution(f"99-potd/01-daily/{Path(__file__).resolve().parent.name}")
count_missing_per_column = _module.count_missing_per_column


def test_example_matches_the_specs_worked_counts():
    columns = ["a", "b"]
    rows = [["1", "NA"], ["NA", "NA"], ["3", "1"], ["NA", "2"]]
    assert count_missing_per_column(columns, rows) == [2, 2]


def test_column_entirely_missing_counts_n():
    columns = ["a"]
    rows = [["NA"], ["NA"], ["NA"]]
    assert count_missing_per_column(columns, rows) == [3]


def test_column_with_zero_missing_is_still_printed():
    columns = ["a", "b"]
    rows = [["1", "2"], ["3", "4"]]
    assert count_missing_per_column(columns, rows) == [0, 0]


def test_near_miss_sentinels_are_not_counted_as_missing():
    columns = ["a"]
    rows = [["N/A"], ["null"], ["NA"], ["na"]]
    # Only the exact literal "NA" (row 3) counts.
    assert count_missing_per_column(columns, rows) == [1]


def test_many_columns_counted_independently():
    columns = ["a", "b", "c"]
    rows = [
        ["NA", "1", "NA"],
        ["2", "NA", "NA"],
        ["3", "4", "5"],
    ]
    assert count_missing_per_column(columns, rows) == [1, 1, 2]
