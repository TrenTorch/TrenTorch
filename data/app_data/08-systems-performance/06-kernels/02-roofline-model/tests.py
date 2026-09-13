"""
pytest data/app_data/08-systems-performance/06-kernels/02-roofline-model/tests.py
"""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[3]))
from _load import load_solution  # noqa: E402

_module = load_solution(f"08-systems-performance/06-kernels/{Path(__file__).resolve().parent.name}")
arithmetic_intensity = _module.arithmetic_intensity
ridge_point = _module.ridge_point
is_memory_bound = _module.is_memory_bound
achievable_flops_per_sec = _module.achievable_flops_per_sec


# --- Basic correctness (the two the "Run" button samples) -----------------


def test_01_arithmetic_intensity_matches_hand_computation():
    assert arithmetic_intensity(flops=100, bytes_moved=25) == 4.0


def test_02_ridge_point_matches_hand_computation():
    assert ridge_point(peak_flops_per_sec=1000.0, peak_bytes_per_sec=100.0) == 10.0


# --- Shape / general-case coverage -----------------------------------


def test_03_low_intensity_computation_is_memory_bound():
    # AI=2, ridge=10 -> well below the ridge point
    assert is_memory_bound(flops=200, bytes_moved=100, peak_flops_per_sec=1000.0, peak_bytes_per_sec=100.0) is True


def test_04_high_intensity_computation_is_compute_bound():
    # AI=50, ridge=10 -> well above the ridge point
    assert is_memory_bound(flops=5000, bytes_moved=100, peak_flops_per_sec=1000.0, peak_bytes_per_sec=100.0) is False


# --- Parameter handling -------------------------------------------------


def test_05_memory_bound_throughput_is_capped_by_intensity_times_bandwidth():
    # AI=2, bandwidth=100 -> achievable = 200, well under peak_flops=1000
    result = achievable_flops_per_sec(
        flops=200, bytes_moved=100, peak_flops_per_sec=1000.0, peak_bytes_per_sec=100.0
    )
    assert result == 200.0


def test_06_compute_bound_throughput_is_capped_at_peak_flops():
    # AI=50, way above the ridge point -> capped at peak_flops=1000, not
    # the (much larger) intensity*bandwidth=5000
    result = achievable_flops_per_sec(
        flops=5000, bytes_moved=100, peak_flops_per_sec=1000.0, peak_bytes_per_sec=100.0
    )
    assert result == 1000.0


# --- Edge cases ---------------------------------------------------------


def test_07_at_exactly_the_ridge_point_is_not_flagged_as_memory_bound():
    # AI == ridge point exactly: both ceilings are hit simultaneously,
    # not "below" the ridge point.
    assert is_memory_bound(flops=1000, bytes_moved=100, peak_flops_per_sec=1000.0, peak_bytes_per_sec=100.0) is False


def test_08_at_exactly_the_ridge_point_achievable_equals_peak_flops():
    result = achievable_flops_per_sec(
        flops=1000, bytes_moved=100, peak_flops_per_sec=1000.0, peak_bytes_per_sec=100.0
    )
    assert result == 1000.0


# --- The actual point of the exercise: why fusion helps one, not the other ---


def test_09_reducing_bytes_moved_helps_a_memory_bound_kernel():
    # Same flops, but fusion (01-kernel-fusion) cuts bytes_moved in half
    # -- a memory-bound kernel's achievable throughput increases
    # proportionally, since it was capped by bandwidth, not compute.
    peak_flops, peak_bandwidth = 1000.0, 100.0
    before = achievable_flops_per_sec(200, 100, peak_flops, peak_bandwidth)  # AI=2
    after = achievable_flops_per_sec(200, 50, peak_flops, peak_bandwidth)  # AI=4, fused
    assert after > before


def test_10_reducing_bytes_moved_does_nothing_for_an_already_compute_bound_kernel():
    # Same halving of bytes_moved, but this kernel was ALREADY
    # compute-bound (capped at peak_flops) -- fusion's memory-traffic
    # reduction has zero effect on its achievable throughput, since
    # compute, not memory, was the bottleneck all along.
    peak_flops, peak_bandwidth = 1000.0, 100.0
    before = achievable_flops_per_sec(5000, 100, peak_flops, peak_bandwidth)  # AI=50
    after = achievable_flops_per_sec(5000, 50, peak_flops, peak_bandwidth)  # AI=100, fused
    assert before == after == peak_flops


# --- Independent correctness oracle -----------------------------------


def test_11_matches_the_published_roofline_model_formula():
    # This is the exact roofline model published in Williams, Waterman
    # & Patterson, "Roofline: An Insightful Visual Performance Model for
    # Multicore Architectures" (2009) -- not our own derivation:
    # attainable GFLOPs/sec = min(peak GFLOPs/sec, peak GB/sec * arithmetic intensity).
    # A realistic example: a GPU with 20 TFLOPs/sec peak compute and
    # 900 GB/sec peak memory bandwidth, running a kernel with AI = 10
    # FLOPs/byte (well below the ~22 FLOPs/byte ridge point for this
    # hardware) should be memory-bound, achieving only 9 TFLOPs/sec.
    peak_flops = 20_000  # GFLOPs/sec, in illustrative round units
    peak_bandwidth = 900  # GB/sec
    ai = 10  # FLOPs/byte
    flops = ai * 1000  # pick bytes_moved=1000 to realize this AI exactly
    bytes_moved = 1000

    assert is_memory_bound(flops, bytes_moved, peak_flops, peak_bandwidth) is True
    result = achievable_flops_per_sec(flops, bytes_moved, peak_flops, peak_bandwidth)
    assert result == 9000  # 10 * 900
