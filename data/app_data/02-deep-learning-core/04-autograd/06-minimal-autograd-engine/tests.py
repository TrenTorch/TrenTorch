"""
pytest data/app_data/02-deep-learning-core/04-autograd/06-minimal-autograd-engine/tests.py
"""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[3]))
from _load import load_solution  # noqa: E402

_module = load_solution(f"02-deep-learning-core/04-autograd/{Path(__file__).resolve().parent.name}")
backward = _module.backward

Value = load_solution("02-deep-learning-core/04-autograd/04-graph-node").Value


def test_backward_sets_root_grad_to_one():
    a = Value(2.0)
    b = Value(3.0)
    c = a + b
    backward(c)
    assert c.grad == 1.0


def test_backward_computes_correct_gradients_for_simple_addition():
    a = Value(2.0)
    b = Value(3.0)
    c = a + b
    backward(c)
    assert a.grad == 1.0
    assert b.grad == 1.0


def test_backward_computes_correct_gradients_for_simple_multiplication():
    a = Value(2.0)
    b = Value(3.0)
    c = a * b
    backward(c)
    assert a.grad == 3.0
    assert b.grad == 2.0


def test_backward_computes_correct_gradients_for_a_multi_step_expression():
    # c = a*b + a, dc/da = b + 1, dc/db = a
    a = Value(2.0)
    b = Value(3.0)
    c = a * b + a
    backward(c)
    assert c.data == 8.0
    assert a.grad == 4.0  # b(3) + 1
    assert b.grad == 2.0  # a(2)


def test_backward_correctly_accumulates_gradient_for_a_reused_variable():
    # y = x * x = x^2, dy/dx = 2x
    x = Value(3.0)
    y = x * x
    backward(y)
    assert y.data == 9.0
    assert x.grad == 6.0  # 2*3


def test_backward_matches_a_more_complex_expression_against_real_pytorch():
    import torch

    tx = torch.tensor(2.0, requires_grad=True)
    ty = torch.tensor(3.0, requires_grad=True)
    tz = tx * tx * ty + ty
    tz.backward()

    x = Value(2.0)
    y = Value(3.0)
    z = x * x * y + y
    backward(z)

    assert abs(z.data - tz.item()) < 1e-9
    assert abs(x.grad - tx.grad.item()) < 1e-9
    assert abs(y.grad - ty.grad.item()) < 1e-9


def test_backward_does_not_process_nodes_out_of_order():
    # Directly targets a mutant that processes nodes in FORWARD
    # topological order instead of reversed: this would call a node's
    # _backward before its own .grad is fully accumulated (still at its
    # default 0.0), producing a silently wrong (zero or partial)
    # gradient for anything with more than one path to the root.
    a = Value(2.0)
    b = a * a  # a used twice within one op
    c = b * a  # a used again here: c = a^3
    backward(c)
    # dc/da = 3*a^2 = 3*4 = 12
    assert abs(a.grad - 12.0) < 1e-9
