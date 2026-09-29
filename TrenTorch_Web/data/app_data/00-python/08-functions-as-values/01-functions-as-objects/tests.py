"""
pytest data/app_data/00-python/08-functions-as-values/01-functions-as-objects/tests.py
"""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[3]))
from _load import load_solution  # noqa: E402

_module = load_solution(f"00-python/08-functions-as-values/{Path(__file__).resolve().parent.name}")
alias_and_call = _module.alias_and_call
apply_selected = _module.apply_selected
same_function = _module.same_function


def test_alias_preserves_the_function_object():
    calls = []

    def record(x):
        calls.append(x)
        return x * 2

    result = alias_and_call(record, 5)
    assert result == 10
    assert calls == [5]


def test_calling_through_an_alias():
    assert alias_and_call(lambda x: x * 2, 5) == 10


def test_function_selection_by_index():
    assert apply_selected([abs, str], 0, -7) == 7
    assert apply_selected([abs, str], 1, 42) == "42"
    assert apply_selected([abs, str], -1, 42) == "42"


def test_identity_rather_than_result_equality():
    def f(x):
        return x

    def g(x):
        return x

    assert same_function(f, f) is True
    assert same_function(f, g) is False
    a = f
    assert same_function(f, a) is True


def test_input_functions_untouched():
    functions = [abs, str]
    apply_selected(functions, 0, -1)
    assert functions == [abs, str]
