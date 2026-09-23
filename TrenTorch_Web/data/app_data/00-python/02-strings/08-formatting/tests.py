"""
pytest data/app_data/00-python/02-strings/08-formatting/tests.py
"""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[3]))
from _load import load_solution  # noqa: E402

_module = load_solution(f"00-python/02-strings/{Path(__file__).resolve().parent.name}")
receipt_line = _module.receipt_line
format_percent = _module.format_percent
format_binary = _module.format_binary
debug_label = _module.debug_label


def test_receipt_line_exact_widths():
    line = receipt_line("Pen", 3, 1.5)
    assert len(line) == 26
    assert line == "Pen            3      1.50"


def test_receipt_line_overflow_not_truncated():
    line = receipt_line("A Very Long Item Name", 1, 1.0)
    assert line.startswith("A Very Long Item Name")


def test_receipt_line_rounding_and_decimals():
    assert receipt_line("X", 1, 2).endswith("2.00")
    assert receipt_line("X", 1, 1.005).endswith(f"{1.005:.2f}")
    assert receipt_line("X", 1, 1234.5).endswith("1234.50")


def test_format_percent_variable_precision():
    assert format_percent(0.256, 1) == "25.6%"
    assert format_percent(0.256, 0) == "26%"
    assert format_percent(0.5, 3) == "50.000%"


def test_format_binary_padding_and_overflow():
    assert format_binary(5, 8) == "00000101"
    assert format_binary(0, 4) == "0000"
    assert format_binary(255, 2) == "11111111"


def test_debug_label_repr_distinction():
    assert debug_label("name", "Ada") == "name='Ada'"
    assert debug_label("n", 5) == "n=5"
