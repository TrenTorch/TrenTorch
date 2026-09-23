"""
pytest data/app_data/00-python/02-strings/11-assemble-sales-report/tests.py
"""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[3]))
from _load import load_solution  # noqa: E402

_module = load_solution(f"00-python/02-strings/{Path(__file__).resolve().parent.name}")
build_sales_report = _module.build_sales_report

RAW = """# comment
  Pen , 3 , 1.5
blue widget deluxe, 1000, 2.5

garbage line without commas
widget, abc, 5.0
café au lait, 2, 3.0
"""


def test_comments_blanks_and_malformed_lines_skipped():
    report = build_sales_report(RAW)
    lines = report.split("\n")
    assert "Rows: 3 " in lines[-1]
    # Only the 3 valid records appear as rows (header + 3 rows + separator +
    # grand total + summary = 7 lines).
    assert len(lines) == 7


def test_whitespace_tolerance_and_comment_with_leading_spaces():
    raw = "   # leading-space comment\n Pen , 3 , 1.5 \n"
    report = build_sales_report(raw)
    assert "Rows: 1 " in report.split("\n")[-1]


def test_title_case_then_truncate():
    raw = "blue widget deluxe, 1, 1.0\n"
    report = build_sales_report(raw)
    row = report.split("\n")[1]
    assert row.startswith("Blue Widget ")
    assert row[:12] == "Blue Widget "


def test_exact_column_alignment():
    raw = "Pen , 3 , 1.5\n"
    report = build_sales_report(raw)
    lines = report.split("\n")
    expected_header = f"{'ITEM':<12}{'QTY':>4}{'PRICE':>10}{'TOTAL':>12}"
    expected_row = f"{'Pen':<12}{3:>4}{1.5:>10.2f}{4.5:>12,.2f}"
    assert lines[0] == expected_header
    assert lines[1] == expected_row
    assert lines[2] == "-" * 38


def test_totals_and_thousands_separators():
    raw = "Widget, 1000, 2.5\n"
    report = build_sales_report(raw)
    lines = report.split("\n")
    expected_row = f"{'Widget':<12}{1000:>4}{2.5:>10.2f}{2500.0:>12,.2f}"
    assert lines[1] == expected_row
    assert "2,500.00" in lines[1]
    expected_grand_total_line = f"{'TOTAL':<26}{2500.0:>12,.2f}"
    assert lines[3] == expected_grand_total_line


def test_byte_count_with_non_ascii_labels():
    raw = "café au lait, 2, 3.0\n"
    report = build_sales_report(raw)
    summary = report.split("\n")[-1]
    # "Café Au Lait" is 12 characters but 13 UTF-8 bytes ('é' is 2 bytes).
    assert "UTF-8 bytes in items: 13" in summary


def test_empty_and_all_invalid_input():
    for raw in ("", "# only a comment\n"):
        report = build_sales_report(raw)
        lines = report.split("\n")
        assert lines[0] == f"{'ITEM':<12}{'QTY':>4}{'PRICE':>10}{'TOTAL':>12}"
        assert lines[1] == "-" * 38
        assert lines[2] == f"{'TOTAL':<26}{0.0:>12,.2f}"
        assert lines[3] == "Rows: 0 | UTF-8 bytes in items: 0"


def test_original_input_unchanged_and_no_valid_record_dropped():
    raw = RAW
    build_sales_report(raw)
    assert raw == RAW
    report = build_sales_report(RAW)
    assert report.split("\n")[-1] == "Rows: 3 | UTF-8 bytes in items: 28"
