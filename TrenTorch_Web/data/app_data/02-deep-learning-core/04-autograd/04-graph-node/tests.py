"""
pytest data/app_data/02-deep-learning-core/04-autograd/04-graph-node/tests.py
"""

import sys
from pathlib import Path

import numpy as np

sys.path.insert(0, str(Path(__file__).resolve().parents[3]))
from _load import load_solution  # noqa: E402

Value = load_solution(f"02-deep-learning-core/04-autograd/{Path(__file__).resolve().parent.name}").Value


def test_value_stores_data():
    v = Value(5.0)
    assert v.data == 5.0
    assert v.grad == 0.0


def test_add_computes_correct_data():
    a = Value(2.0)
    b = Value(3.0)
    c = a + b
    assert c.data == 5.0


def test_mul_computes_correct_data():
    a = Value(2.0)
    b = Value(3.0)
    c = a * b
    assert c.data == 6.0


def test_add_records_parents_in_prev():
    a = Value(2.0)
    b = Value(3.0)
    c = a + b
    assert c._prev == {a, b}


def test_add_backward_pushes_gradient_to_both_parents():
    a = Value(2.0)
    b = Value(3.0)
    c = a + b
    c.grad = 1.0
    c._backward()
    assert a.grad == 1.0
    assert b.grad == 1.0


def test_mul_backward_pushes_correct_gradient_to_each_parent():
    a = Value(2.0)
    b = Value(3.0)
    c = a * b
    c.grad = 1.0
    c._backward()
    assert a.grad == 3.0  # b's data
    assert b.grad == 2.0  # a's data


def test_backward_scales_with_out_grad():
    a = Value(2.0)
    b = Value(3.0)
    c = a * b
    c.grad = 5.0
    c._backward()
    assert a.grad == 15.0
    assert b.grad == 10.0


def test_operations_accept_a_plain_number_not_just_a_value():
    a = Value(2.0)
    c = a + 3.0
    assert c.data == 5.0
    d = a * 4.0
    assert d.data == 8.0


def test_backward_accumulates_when_the_same_value_is_used_twice():
    # A node used in TWO places (here, both operands of the same
    # addition are the same object) must accumulate contributions from
    # BOTH uses, not just overwrite with the last one.
    x = Value(5.0)
    y = x + x
    y.grad = 1.0
    y._backward()
    assert x.grad == 2.0  # 1.0 from each of the two uses


def test_backward_accumulates_across_a_chain_using_the_same_variable_twice():
    x = Value(3.0)
    y = x * x  # x used twice: y = x^2
    y.grad = 1.0
    y._backward()
    # d(x*x)/dx = x (from "self" slot) + x (from "other" slot) = 2x = 6.0
    assert x.grad == 6.0


def test_backward_does_not_overwrite_pre_existing_gradient():
    # Directly targets a mutant that uses `=` instead of `+=` inside
    # _backward: a node that already has a nonzero .grad (from some
    # earlier accumulation) must have the new contribution ADDED, not
    # replace what was already there.
    a = Value(2.0)
    b = Value(3.0)
    a.grad = 100.0  # simulate a prior accumulated contribution
    c = a + b
    c.grad = 1.0
    c._backward()
    assert a.grad == 101.0  # 100.0 (pre-existing) + 1.0 (this contribution)
    assert a.grad != 1.0
