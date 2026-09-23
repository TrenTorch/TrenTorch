"""
pytest data/app_data/00-python/01-core-semantics/01-what-a-variable-is/tests.py
"""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[3]))
from _load import load_solution  # noqa: E402

_module = load_solution(f"00-python/01-core-semantics/{Path(__file__).resolve().parent.name}")
compute_total = _module.compute_total
swap_two_variables = _module.swap_two_variables


def test_compute_total_correct_arithmetic():
    # 10 * 3 = 30 subtotal, 8% tax = 2.4, total = 32.4
    assert compute_total(10, 3) == 32.4


def test_compute_total_correct_arithmetic_second_case():
    assert round(compute_total(50, 2), 2) == 108.0


def test_compute_total_uses_plus_equals_correctly():
    # Tax must be ADDED to the original subtotal, not replace it.
    result = compute_total(100, 1)
    assert result == 108.0
    assert result != 8.0


def test_swap_two_variables_returns_correct_order():
    assert swap_two_variables(1, 2) == (2, 1)
    assert swap_two_variables("a", "b") == ("b", "a")


def test_swap_two_variables_handles_equal_inputs():
    assert swap_two_variables(5, 5) == (5, 5)
