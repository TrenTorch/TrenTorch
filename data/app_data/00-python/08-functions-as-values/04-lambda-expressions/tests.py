"""
pytest data/app_data/00-python/08-functions-as-values/04-lambda-expressions/tests.py
"""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[3]))
from _load import load_solution  # noqa: E402

_module = load_solution(f"00-python/08-functions-as-values/{Path(__file__).resolve().parent.name}")
make_square_function = _module.make_square_function
make_offset_function = _module.make_offset_function
apply_lambda = _module.apply_lambda


def test_returned_object_is_callable():
    square = make_square_function()
    assert callable(square)


def test_lambda_computation():
    square = make_square_function()
    assert square(6) == 36
    assert square(0) == 0


def test_captured_offset():
    add_five = make_offset_function(5)
    add_ten = make_offset_function(10)
    assert add_five(10) == 15
    assert add_ten(10) == 20


def test_works_with_externally_supplied_functions():
    assert apply_lambda([1, 2, 3], abs) == [1, 2, 3]
    assert apply_lambda([1, 2, 3], lambda x: x * 2) == [2, 4, 6]


def test_input_preservation():
    values = [1, 2, 3]
    apply_lambda(values, lambda x: x * 2)
    assert values == [1, 2, 3]
