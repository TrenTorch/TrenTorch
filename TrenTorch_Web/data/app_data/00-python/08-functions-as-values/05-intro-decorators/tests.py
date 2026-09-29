"""
pytest data/app_data/00-python/08-functions-as-values/05-intro-decorators/tests.py
"""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[3]))
from _load import load_solution  # noqa: E402

_module = load_solution(f"00-python/08-functions-as-values/{Path(__file__).resolve().parent.name}")
add_call_count = _module.add_call_count
run_with_message = _module.run_with_message
decorate_result = _module.decorate_result


def test_original_function_called_exactly_once():
    calls = []

    def record(x):
        calls.append(x)
        return x

    run_with_message(record, "msg", 5)
    assert calls == [5]


def test_return_value_preserved():
    def add(a, b):
        return a + b

    wrapped = add_call_count(add)
    assert wrapped(2, 3) == 5


def test_positional_and_keyword_forwarding():
    def add(a, b):
        return a + b

    assert run_with_message(add, "msg", 2, b=3) == 5
    wrapped = add_call_count(add)
    assert wrapped(2, b=3) == 5


def test_independent_call_counts():
    def add(a, b):
        return a + b

    def sub(a, b):
        return a - b

    wrapped_add = add_call_count(add)
    wrapped_sub = add_call_count(sub)
    wrapped_add(1, 1)
    wrapped_add(1, 1)
    wrapped_sub(1, 1)
    assert wrapped_add.calls == 2
    assert wrapped_sub.calls == 1


def test_arguments_not_modified():
    def add(a, b):
        return a + b

    args = (2, 3)
    run_with_message(add, "msg", *args)
    assert args == (2, 3)


def test_result_transformation():
    def name(x):
        return x

    wrapped = decorate_result(name, "Name: ")
    assert wrapped("Ada") == "Name: Ada"
