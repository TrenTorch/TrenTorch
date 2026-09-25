"""
pytest data/app_data/00-python/08-functions-as-values/03-closures/tests.py
"""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[3]))
from _load import load_solution  # noqa: E402

_module = load_solution(f"00-python/08-functions-as-values/{Path(__file__).resolve().parent.name}")
make_multiplier = _module.make_multiplier
make_prefixer = _module.make_prefixer
make_counter = _module.make_counter


def test_retained_value():
    double = make_multiplier(2)
    assert double(7) == 14


def test_independent_closures():
    double = make_multiplier(2)
    triple = make_multiplier(3)
    assert double(5) == 10
    assert triple(5) == 15


def test_multiple_calls_use_same_retained_value():
    add_five = make_prefixer("ERROR: ")
    assert add_five("disk full") == "ERROR: disk full"
    assert add_five("timeout") == "ERROR: timeout"


def test_counter_state():
    counter = make_counter(10)
    assert counter() == 11
    assert counter() == 12


def test_independent_counter_state():
    a = make_counter(0)
    b = make_counter(0)
    assert a() == 1
    assert a() == 2
    assert b() == 1


def test_no_global_state_across_factory_calls():
    m1 = make_multiplier(10)
    m2 = make_multiplier(100)
    assert m1(1) == 10
    assert m2(1) == 100
    assert m1(1) == 10
