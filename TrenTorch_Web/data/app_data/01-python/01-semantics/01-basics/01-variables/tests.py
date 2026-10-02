"""
pytest tests.py
"""

from _load import load_solution

_module = load_solution(__file__)
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
