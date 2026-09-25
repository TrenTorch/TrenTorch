"""
pytest data/app_data/00-python/12-bridging-to-numpy-ml/01-interpreter-mechanics/tests.py
"""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[3]))
from _load import load_solution  # noqa: E402

_module = load_solution(f"00-python/12-bridging-to-numpy-ml/{Path(__file__).resolve().parent.name}")
dot_loop = _module.dot_loop
loop_time_model = _module.loop_time_model
vectorized_time_model = _module.vectorized_time_model
break_even_n = _module.break_even_n
list_of_ints_bytes = _module.list_of_ints_bytes
typed_array_bytes = _module.typed_array_bytes


def test_dot_loop_correctness():
    assert dot_loop([1, 2, 3], [4, 5, 6]) == 32
    assert dot_loop([-1, 2], [3, -4]) == -11
    assert dot_loop([5], [5]) == 25
    assert dot_loop([], []) == 0.0


def test_cost_model_formulas():
    assert loop_time_model(10, 2) == 20
    assert loop_time_model(0, 2) == 0.0
    assert vectorized_time_model(10, 5, 1) == 15
    assert vectorized_time_model(0, 5, 1) == 5


def test_break_even_n_exact_threshold():
    n = break_even_n(per_iteration_cost=3, call_overhead=7, per_element_cost=1)
    assert n == 4
    assert vectorized_time_model(n, 7, 1) <= loop_time_model(n, 3)
    assert vectorized_time_model(n - 1, 7, 1) > loop_time_model(n - 1, 3)


def test_break_even_n_edge_cases():
    assert break_even_n(per_iteration_cost=1, call_overhead=5, per_element_cost=2) is None
    assert break_even_n(per_iteration_cost=1, call_overhead=1, per_element_cost=1) is None
    assert break_even_n(per_iteration_cost=3, call_overhead=0, per_element_cost=1) == 1


def test_storage_estimates():
    assert list_of_ints_bytes(0) == 0
    assert typed_array_bytes(0, 8) == 0
    assert list_of_ints_bytes(1) == 36
    assert typed_array_bytes(1000, 8) == 8000
    assert list_of_ints_bytes(1000) == 4.5 * typed_array_bytes(1000, 8)
