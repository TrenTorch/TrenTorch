"""
pytest data/app_data/06-inference/03-quantization-and-numerical-efficiency/05-prefill-decode-roofline-analysis/tests.py
"""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[3]))
from _load import load_solution  # noqa: E402

roofline_analysis = load_solution(
    f"06-inference/03-quantization-and-numerical-efficiency/{Path(__file__).resolve().parent.name}"
).roofline_analysis


def test_compute_bound_example():
    result = roofline_analysis(
        peak_flops_per_sec=100e12, peak_bytes_per_sec=2e12,
        prefill_flops=4e9, prefill_bytes=1e6,
        decode_flops=4e9, decode_bytes=1e6,
    )
    p = result["prefill"]
    assert p["classification"] == "compute_bound"
    assert abs(p["arithmetic_intensity"] - 4000) < 1e-6
    assert abs(p["ridge_point"] - 50) < 1e-6


def test_typical_prefill_compute_decode_memory():
    result = roofline_analysis(
        peak_flops_per_sec=300e12, peak_bytes_per_sec=3e12,
        prefill_flops=2e12, prefill_bytes=4e9,
        decode_flops=2e9, decode_bytes=4e9,
    )
    assert result["prefill"]["classification"] == "compute_bound"
    assert result["decode"]["classification"] == "memory_bound"


def test_zero_bytes_moved_is_pure_compute():
    result = roofline_analysis(
        peak_flops_per_sec=50e12, peak_bytes_per_sec=1e12,
        prefill_flops=1e9, prefill_bytes=0,
        decode_flops=1e6, decode_bytes=0,
    )
    assert result["prefill"]["memory_time_s"] == 0.0
    assert result["prefill"]["classification"] == "compute_bound"
    assert result["prefill"]["arithmetic_intensity"] == float("inf")


def test_predicted_time_is_max_of_the_two():
    result = roofline_analysis(
        peak_flops_per_sec=10.0, peak_bytes_per_sec=10.0,
        prefill_flops=100.0, prefill_bytes=5.0,
        decode_flops=1.0, decode_bytes=50.0,
    )
    p, d = result["prefill"], result["decode"]
    assert p["predicted_time_s"] == max(p["compute_time_s"], p["memory_time_s"])
    assert d["predicted_time_s"] == max(d["compute_time_s"], d["memory_time_s"])
    assert d["classification"] == "memory_bound"
