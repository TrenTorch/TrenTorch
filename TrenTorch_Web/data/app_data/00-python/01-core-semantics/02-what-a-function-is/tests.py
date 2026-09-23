"""
pytest data/app_data/00-python/01-core-semantics/02-what-a-function-is/tests.py
"""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[3]))
from _load import load_solution  # noqa: E402

_module = load_solution(f"00-python/01-core-semantics/{Path(__file__).resolve().parent.name}")
is_even = _module.is_even
greet_formal = _module.greet_formal
apply_twice = _module.apply_twice


def test_is_even_across_cases():
    assert is_even(4) is True
    assert is_even(7) is False
    assert is_even(0) is True
    assert is_even(-4) is True
    assert is_even(-3) is False


def test_greet_formal_exact_format():
    assert greet_formal("Smith", "Dr.") == "Good day, Dr. Smith."
    assert greet_formal("Lee", "Ms.") == "Good day, Ms. Lee."


def test_apply_twice_calls_function_exactly_twice_in_sequence():
    calls = []

    def record_and_increment(x):
        calls.append(x)
        return x + 1

    result = apply_twice(record_and_increment, 5)
    assert result == 7
    assert calls == [5, 6]


def test_apply_twice_with_function_returning_none():
    def returns_none(_x):
        return None

    assert apply_twice(returns_none, 10) is None
