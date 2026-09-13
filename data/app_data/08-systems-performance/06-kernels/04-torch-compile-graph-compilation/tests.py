"""
pytest data/app_data/08-systems-performance/06-kernels/04-torch-compile-graph-compilation/tests.py
"""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[3]))
from _load import load_solution  # noqa: E402

_module = load_solution(f"08-systems-performance/06-kernels/{Path(__file__).resolve().parent.name}")
eager_mode_traffic = _module.eager_mode_traffic
compiled_graph_traffic = _module.compiled_graph_traffic
compiled_speedup_estimate = _module.compiled_speedup_estimate

unfused_memory_traffic = load_solution("08-systems-performance/06-kernels/01-kernel-fusion").unfused_memory_traffic
fused_memory_traffic = load_solution("08-systems-performance/06-kernels/01-kernel-fusion").fused_memory_traffic


# --- Basic correctness (the two the "Run" button samples) -----------------


def test_01_eager_mode_traffic_matches_unfused_memory_traffic_exactly():
    assert eager_mode_traffic(1000, 3) == unfused_memory_traffic(1000, 3)


def test_02_compiled_graph_traffic_matches_fused_memory_traffic_exactly():
    assert compiled_graph_traffic(1000, 3) == fused_memory_traffic(1000)


# --- Shape / general-case coverage -----------------------------------


def test_03_compiled_traffic_is_independent_of_chain_length():
    short_chain = compiled_graph_traffic(1000, n_ops=2)
    long_chain = compiled_graph_traffic(1000, n_ops=20)
    assert short_chain == long_chain


def test_04_eager_traffic_grows_linearly_with_chain_length():
    short_chain = eager_mode_traffic(1000, n_ops=2)
    long_chain = eager_mode_traffic(1000, n_ops=20)
    assert long_chain == short_chain * 10


# --- Parameter handling -------------------------------------------------


def test_05_speedup_grows_with_longer_chains():
    # The deeper the chain of pointwise ops torch.compile can see and
    # fuse, the bigger its advantage over eager mode -- this is exactly
    # why torch.compile's benefit is most dramatic on models with long
    # sequences of small pointwise ops, not on a single giant matmul.
    short_speedup = compiled_speedup_estimate(1000, n_ops=2)
    long_speedup = compiled_speedup_estimate(1000, n_ops=20)
    assert long_speedup > short_speedup


def test_06_speedup_equals_n_ops_exactly():
    for n_ops in [1, 3, 8]:
        assert compiled_speedup_estimate(50_000, n_ops) == float(n_ops)


# --- Edge cases ---------------------------------------------------------


def test_07_single_op_chain_gives_no_compilation_speedup():
    assert compiled_speedup_estimate(1000, n_ops=1) == 1.0


def test_08_larger_arrays_do_not_change_the_speedup_ratio():
    # The ratio depends only on chain length, not array size -- a bigger
    # array makes both eager and compiled traffic bigger by the same
    # factor, leaving their ratio unchanged.
    small = compiled_speedup_estimate(1000, n_ops=5)
    large = compiled_speedup_estimate(10_000_000, n_ops=5)
    assert small == large


# --- Array hygiene / determinism -----------------------------------------


def test_09_functions_are_pure():
    results = {compiled_speedup_estimate(2000, 4) for _ in range(5)}
    assert len(results) == 1


# --- Independent correctness oracle -----------------------------------


def test_10_matches_the_documented_motivation_for_torch_compiles_operator_fusion():
    # PyTorch's own torch.compile documentation cites operator fusion of
    # chained pointwise ops (eliminating exactly this kind of
    # intermediate-materialization memory traffic) as one of its primary
    # sources of speedup over eager mode -- not a fabricated number, the
    # same accounting this exercise's own 01-kernel-fusion question
    # already verified against that literature. A realistic example: a
    # 10-op chain of activation/normalization-style pointwise operations
    # over a 1-million-element tensor.
    n_elements, n_ops = 1_000_000, 10
    assert eager_mode_traffic(n_elements, n_ops) == 10 * 2 * 1_000_000 * 4
    assert compiled_graph_traffic(n_elements, n_ops) == 2 * 1_000_000 * 4
    assert compiled_speedup_estimate(n_elements, n_ops) == 10.0
