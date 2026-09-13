"""
pytest data/app_data/08-systems-performance/06-kernels/05-torchscript-onnx-export/tests.py
"""

import math
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[3]))
from _load import load_solution  # noqa: E402

_module = load_solution(f"08-systems-performance/06-kernels/{Path(__file__).resolve().parent.name}")
eager_python_dispatch_overhead = _module.eager_python_dispatch_overhead
graph_mode_dispatch_overhead = _module.graph_mode_dispatch_overhead
graph_mode_speedup_estimate = _module.graph_mode_speedup_estimate


# --- Basic correctness (the two the "Run" button samples) -----------------


def test_01_eager_overhead_matches_hand_computation():
    # 100 ops, 1 microsecond each -> 100 microseconds total
    assert math.isclose(eager_python_dispatch_overhead(100, 1e-6), 1e-4)


def test_02_graph_mode_overhead_is_a_single_dispatch_regardless_of_op_count():
    assert graph_mode_dispatch_overhead(1e-6) == 1e-6


# --- Shape / general-case coverage -----------------------------------


def test_03_eager_overhead_scales_linearly_with_op_count():
    small_model = eager_python_dispatch_overhead(50, 1e-6)
    large_model = eager_python_dispatch_overhead(500, 1e-6)
    assert large_model == small_model * 10


def test_04_graph_mode_overhead_never_changes_with_op_count():
    # graph_mode_dispatch_overhead doesn't even take num_ops as an
    # argument -- it genuinely cannot depend on it.
    assert graph_mode_dispatch_overhead(1e-6) == graph_mode_dispatch_overhead(1e-6)


# --- Parameter handling -------------------------------------------------


def test_05_deeper_models_benefit_more_from_graph_mode():
    # The more ops a real model's forward pass calls (a deeper
    # network), the more dispatch overhead eager mode accumulates --
    # and the bigger graph mode's relative advantage becomes.
    shallow_speedup = graph_mode_speedup_estimate(num_ops=10, per_op_dispatch_seconds=1e-6)
    deep_speedup = graph_mode_speedup_estimate(num_ops=1000, per_op_dispatch_seconds=1e-6)
    assert deep_speedup > shallow_speedup


def test_06_speedup_equals_num_ops_exactly():
    for num_ops in [1, 50, 500]:
        assert math.isclose(graph_mode_speedup_estimate(num_ops, 1e-6), float(num_ops))


# --- Edge cases ---------------------------------------------------------


def test_07_single_op_model_gains_nothing_from_graph_mode():
    assert graph_mode_speedup_estimate(num_ops=1, per_op_dispatch_seconds=1e-6) == 1.0


def test_08_larger_per_op_overhead_scales_both_functions_proportionally_leaving_ratio_unchanged():
    speedup_fast_dispatch = graph_mode_speedup_estimate(100, per_op_dispatch_seconds=1e-7)
    speedup_slow_dispatch = graph_mode_speedup_estimate(100, per_op_dispatch_seconds=1e-5)
    assert speedup_fast_dispatch == speedup_slow_dispatch


# --- Array hygiene / determinism -----------------------------------------


def test_09_functions_are_pure():
    results = {graph_mode_speedup_estimate(200, 1e-6) for _ in range(5)}
    assert len(results) == 1


# --- Independent correctness oracle -----------------------------------


def test_10_matches_the_documented_motivation_for_avoiding_eager_python_in_production_serving():
    # This is the exact, published motivation for TorchScript and ONNX
    # export -- PyTorch's own deployment documentation cites eliminating
    # per-op Python dispatch overhead (not model compute itself) as the
    # specific benefit of exporting a graph rather than serving eager
    # Python directly. A realistic example: a 200-layer model where each
    # op's dispatch overhead is a modest 2 microseconds (a real, typical
    # order of magnitude for PyTorch's eager dispatch cost) -- eager mode
    # pays 400 microseconds of PURE dispatch overhead per forward pass,
    # before any actual computation, that a compiled graph pays only
    # once.
    num_ops, per_op_overhead = 200, 2e-6
    eager = eager_python_dispatch_overhead(num_ops, per_op_overhead)
    graph = graph_mode_dispatch_overhead(per_op_overhead)
    assert math.isclose(eager, 4e-4)
    assert graph == 2e-6
    assert math.isclose(graph_mode_speedup_estimate(num_ops, per_op_overhead), 200.0)
