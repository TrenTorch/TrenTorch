"""
pytest data/app_data/08-systems-performance/06-kernels/01-kernel-fusion/tests.py
"""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[3]))
from _load import load_solution  # noqa: E402

_module = load_solution(f"08-systems-performance/06-kernels/{Path(__file__).resolve().parent.name}")
unfused_memory_traffic = _module.unfused_memory_traffic
fused_memory_traffic = _module.fused_memory_traffic
fusion_speedup_estimate = _module.fusion_speedup_estimate


# --- Basic correctness (the two the "Run" button samples) -----------------


def test_01_unfused_traffic_matches_hand_computation():
    # 2 ops, 1000 elements, 4 bytes: each op reads 1000*4=4000 bytes and
    # writes another 4000 bytes (8000 per op), times 2 ops = 16000.
    assert unfused_memory_traffic(1000, 2, bytes_per_element=4) == 16000


def test_02_fused_traffic_matches_hand_computation():
    # one read + one write of 1000 elements at 4 bytes = 8000, regardless of op count.
    assert fused_memory_traffic(1000, bytes_per_element=4) == 8000


# --- Shape / general-case coverage -----------------------------------


def test_03_unfused_traffic_scales_linearly_with_number_of_ops():
    two_ops = unfused_memory_traffic(1000, 2)
    four_ops = unfused_memory_traffic(1000, 4)
    assert four_ops == two_ops * 2


def test_04_fused_traffic_is_independent_of_the_number_of_ops_chained():
    # This is the entire point: fusing more ops together costs NOTHING
    # extra in memory traffic, only in (typically much cheaper) compute.
    assert fused_memory_traffic(1000) == fused_memory_traffic(1000)


# --- Parameter handling -------------------------------------------------


def test_05_speedup_estimate_matches_ratio_of_the_two_traffic_functions():
    n_elements, n_ops = 5000, 3
    expected = unfused_memory_traffic(n_elements, n_ops) / fused_memory_traffic(n_elements)
    assert fusion_speedup_estimate(n_elements, n_ops) == expected


def test_06_speedup_estimate_equals_n_ops_exactly():
    # Since fused traffic never depends on n_ops, the speedup ratio
    # reduces to exactly n_ops (fusing k ops together saves a factor of
    # k in memory traffic, precisely because each unfused op pays the
    # same fixed read+write cost).
    for n_ops in [1, 2, 5, 10]:
        assert fusion_speedup_estimate(10_000, n_ops) == float(n_ops)


# --- Edge cases ---------------------------------------------------------


def test_07_single_op_gives_no_speedup():
    assert fusion_speedup_estimate(1000, n_ops=1) == 1.0


def test_08_larger_dtype_scales_both_traffic_functions_proportionally():
    fp32_unfused = unfused_memory_traffic(1000, 2, bytes_per_element=4)
    fp64_unfused = unfused_memory_traffic(1000, 2, bytes_per_element=8)
    assert fp64_unfused == fp32_unfused * 2


# --- Array hygiene / determinism -----------------------------------------


def test_09_functions_are_pure_same_inputs_always_give_the_same_output():
    results = {unfused_memory_traffic(1000, 3) for _ in range(5)}
    assert len(results) == 1


# --- Independent correctness oracle -----------------------------------


def test_10_matches_the_standard_memory_traffic_accounting_used_to_justify_fusion():
    # This is the exact accounting real fusion literature and framework
    # documentation (e.g. NVIDIA's own kernel-fusion guidance, PyTorch's
    # torch.compile design docs) use to justify fusion's benefit: for a
    # chain of k pointwise ops over n elements, an eager/unfused
    # execution moves 2kn elements of memory traffic (k reads + k writes,
    # each n elements), while a single fused kernel moves only 2n
    # (one read of the original input, one write of the final output).
    # A realistic example: 5 chained ops over a 1-million-element
    # float32 tensor.
    n_elements, n_ops, bytes_per_element = 1_000_000, 5, 4
    unfused = unfused_memory_traffic(n_elements, n_ops, bytes_per_element)
    fused = fused_memory_traffic(n_elements, bytes_per_element)
    assert unfused == 5 * 2 * 1_000_000 * 4
    assert fused == 2 * 1_000_000 * 4
    assert fusion_speedup_estimate(n_elements, n_ops, bytes_per_element) == 5.0
