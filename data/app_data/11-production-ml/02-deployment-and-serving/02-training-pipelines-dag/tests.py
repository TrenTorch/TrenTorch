"""
pytest data/app_data/11-production-ml/02-deployment-and-serving/02-training-pipelines-dag/tests.py
"""

import sys
from pathlib import Path

import pytest

sys.path.insert(0, str(Path(__file__).resolve().parents[3]))
from _load import load_solution  # noqa: E402

_module = load_solution(f"11-production-ml/02-deployment-and-serving/{Path(__file__).resolve().parent.name}")
create_dag = _module.create_dag
add_task = _module.add_task
topological_order = _module.topological_order
has_cycle = _module.has_cycle


# --- Basic correctness (the two the "Run" button samples) -----------------


def test_01_topological_order_respects_dependencies():
    dag = create_dag()
    add_task(dag, "load_data")
    add_task(dag, "clean_data", depends_on=["load_data"])
    add_task(dag, "train", depends_on=["clean_data"])
    order = topological_order(dag)
    assert order.index("load_data") < order.index("clean_data") < order.index("train")


def test_02_cycle_is_detected():
    dag = create_dag()
    add_task(dag, "a", depends_on=["b"])
    add_task(dag, "b", depends_on=["a"])
    assert has_cycle(dag)


# --- General-case coverage --------------------------------------------


def test_03_diamond_shaped_dependencies_resolve_correctly():
    dag = create_dag()
    add_task(dag, "load_data")
    add_task(dag, "clean_data", depends_on=["load_data"])
    add_task(dag, "featurize_a", depends_on=["clean_data"])
    add_task(dag, "featurize_b", depends_on=["clean_data"])
    add_task(dag, "train", depends_on=["featurize_a", "featurize_b"])
    order = topological_order(dag)
    assert order.index("clean_data") < order.index("featurize_a")
    assert order.index("clean_data") < order.index("featurize_b")
    assert order.index("featurize_a") < order.index("train")
    assert order.index("featurize_b") < order.index("train")


def test_04_deterministic_tie_breaking_is_alphabetical():
    dag = create_dag()
    add_task(dag, "zebra")
    add_task(dag, "apple")
    add_task(dag, "mango")
    assert topological_order(dag) == ["apple", "mango", "zebra"]


def test_05_no_cycle_for_a_valid_linear_chain():
    dag = create_dag()
    add_task(dag, "a")
    add_task(dag, "b", depends_on=["a"])
    add_task(dag, "c", depends_on=["b"])
    assert not has_cycle(dag)


# --- Parameter handling -------------------------------------------------


def test_06_task_with_no_dependencies_defaults_to_empty_list():
    dag = create_dag()
    add_task(dag, "solo")
    assert dag["solo"] == []


def test_07_topological_order_includes_every_task_exactly_once():
    dag = create_dag()
    for name in ["a", "b", "c", "d"]:
        add_task(dag, name)
    add_task(dag, "e", depends_on=["a", "b", "c", "d"])
    order = topological_order(dag)
    assert sorted(order) == ["a", "b", "c", "d", "e"]
    assert len(order) == len(set(order))


# --- Edge cases ---------------------------------------------------------


def test_08_empty_dag_has_an_empty_order():
    assert topological_order(create_dag()) == []


def test_09_self_dependency_is_a_cycle():
    dag = create_dag()
    add_task(dag, "a", depends_on=["a"])
    assert has_cycle(dag)


# --- Independent correctness oracle -----------------------------------


def test_10_topological_order_raises_rather_than_silently_dropping_cyclic_tasks():
    # Directly targets a mutant that silently returns a PARTIAL order
    # (just the tasks it managed to process) instead of raising when a
    # genuine cycle exists -- a partial pipeline order is far more
    # dangerous than an explicit failure.
    dag = create_dag()
    add_task(dag, "start")
    add_task(dag, "a", depends_on=["start", "c"])
    add_task(dag, "b", depends_on=["a"])
    add_task(dag, "c", depends_on=["b"])
    with pytest.raises(ValueError):
        topological_order(dag)
