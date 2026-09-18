"""
pytest data/app_data/02-deep-learning-core/04-autograd/05-topological-sort/tests.py
"""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[3]))
from _load import load_solution  # noqa: E402

_module = load_solution(f"02-deep-learning-core/04-autograd/{Path(__file__).resolve().parent.name}")
build_topo_order = _module.build_topo_order

Value = load_solution("02-deep-learning-core/04-autograd/04-graph-node").Value


def test_topo_order_of_a_single_leaf_is_just_itself():
    a = Value(5.0)
    result = build_topo_order(a)
    assert result == [a]


def test_topo_order_puts_root_last():
    a = Value(2.0)
    b = Value(3.0)
    c = a + b
    result = build_topo_order(c)
    assert result[-1] is c


def test_topo_order_puts_every_parent_before_its_child():
    a = Value(2.0)
    b = Value(3.0)
    c = a + b
    result = build_topo_order(c)
    assert result.index(a) < result.index(c)
    assert result.index(b) < result.index(c)


def test_topo_order_handles_a_multi_level_graph():
    a = Value(2.0)
    b = Value(3.0)
    m = a * b  # intermediate node
    c = m + a  # a used again here
    result = build_topo_order(c)
    assert result.index(a) < result.index(m)
    assert result.index(b) < result.index(m)
    assert result.index(m) < result.index(c)
    assert result.index(a) < result.index(c)
    assert result[-1] is c


def test_topo_order_includes_each_node_exactly_once():
    # a is used in two different places; it must still appear exactly
    # once in the topological order, not twice.
    a = Value(2.0)
    b = Value(3.0)
    c = a * b + a
    result = build_topo_order(c)
    assert result.count(a) == 1


def test_topo_order_length_matches_the_number_of_distinct_nodes():
    a = Value(2.0)
    b = Value(3.0)
    m = a * b
    c = m + a
    result = build_topo_order(c)
    # distinct nodes reachable: a, b, m, c = 4
    assert len(result) == 4


def test_topo_order_does_not_append_before_recursing_into_parents():
    # Directly targets a mutant that appends the current node BEFORE
    # recursing into its parents (a pre-order instead of post-order
    # traversal): this would put a parent AFTER its own child in the
    # result, violating the dependency ordering entirely.
    a = Value(2.0)
    b = Value(3.0)
    c = a + b
    d = c * a
    result = build_topo_order(d)
    assert result.index(c) < result.index(d)
    assert result.index(a) < result.index(c)
    assert result[-1] is d
