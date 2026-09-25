"""
pytest data/app_data/00-python/10-object-oriented-programming/03-why-methods-take-self/tests.py
"""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[3]))
from _load import load_solution  # noqa: E402

_module = load_solution(
    f"00-python/10-object-oriented-programming/{Path(__file__).resolve().parent.name}"
)
Accumulator = _module.Accumulator
add_via_class = _module.add_via_class
bound_method_target = _module.bound_method_target
chain_adds = _module.chain_adds


def test_add_returns_same_instance_and_chains():
    a = Accumulator()
    result = a.add(1)
    assert result is a
    assert a.add(1).add(2).value() == 4


def test_instances_keep_separate_totals():
    a = Accumulator()
    b = Accumulator()
    a.add(10)
    assert b.value() == 0


def test_add_via_class_equals_ordinary_call():
    a = Accumulator()
    add_via_class(a, 5)
    assert a.value() == 5


def test_bound_method_target_returns_instance():
    a = Accumulator()
    assert bound_method_target(a.add) is a


def test_chain_adds_and_empty_input():
    a = Accumulator()
    result = chain_adds(a, [1, 2, 3])
    assert result is a
    assert a.value() == 6

    b = Accumulator()
    chain_adds(b, [])
    assert b.value() == 0
