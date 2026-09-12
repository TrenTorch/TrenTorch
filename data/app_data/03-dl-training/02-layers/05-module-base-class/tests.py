"""
pytest data/app_data/03-dl-training/02-layers/05-module-base-class/tests.py
"""

import sys
from pathlib import Path

import numpy as np

sys.path.insert(0, str(Path(__file__).resolve().parents[3]))
from _load import load_solution  # noqa: E402

_module = load_solution(f"03-dl-training/02-layers/{Path(__file__).resolve().parent.name}")
Module = _module.Module


def test_parameters_returns_directly_registered_parameters():
    m = Module()
    w = np.array([1.0, 2.0])
    b = np.array([0.5])
    m.register_parameter("weight", w)
    m.register_parameter("bias", b)
    params = m.parameters()
    assert len(params) == 2
    assert any(np.array_equal(p, w) for p in params)
    assert any(np.array_equal(p, b) for p in params)


def test_parameters_is_empty_for_a_freshly_constructed_module():
    m = Module()
    assert m.parameters() == []


def test_parameters_includes_a_single_child_modules_parameters():
    parent = Module()
    child = Module()
    child.register_parameter("weight", np.array([1.0]))
    parent.register_module("layer1", child)
    params = parent.parameters()
    assert len(params) == 1
    assert np.array_equal(params[0], np.array([1.0]))


def test_parameters_combines_own_and_child_parameters():
    parent = Module()
    parent.register_parameter("own_param", np.array([9.0]))
    child = Module()
    child.register_parameter("weight", np.array([1.0]))
    parent.register_module("layer1", child)
    params = parent.parameters()
    assert len(params) == 2


def test_parameters_recurses_through_multiple_levels_of_nesting():
    grandparent = Module()
    parent = Module()
    child = Module()
    child.register_parameter("deep_param", np.array([42.0]))
    parent.register_module("mid", child)
    grandparent.register_module("top", parent)
    params = grandparent.parameters()
    assert len(params) == 1
    assert np.array_equal(params[0], np.array([42.0]))


def test_parameters_collects_from_multiple_sibling_children():
    parent = Module()
    child1 = Module()
    child1.register_parameter("w1", np.array([1.0]))
    child2 = Module()
    child2.register_parameter("w2", np.array([2.0]))
    parent.register_module("layer1", child1)
    parent.register_module("layer2", child2)
    params = parent.parameters()
    assert len(params) == 2
    values = sorted(p.item() for p in params)
    assert values == [1.0, 2.0]


def test_parameters_recurses_into_children_not_just_reads_their_dict_directly():
    # Directly targets a mutant that reaches into
    # child._parameters.values() directly instead of calling
    # child.parameters(): this would silently miss any parameters that
    # live TWO OR MORE levels deep, since it never recurses further.
    grandparent = Module()
    parent = Module()
    child = Module()
    child.register_parameter("very_deep", np.array([7.0]))
    parent.register_module("mid", child)
    grandparent.register_module("top", parent)
    params = grandparent.parameters()
    assert len(params) == 1
