"""
pytest data/app_data/10-rl-alignment/04-benchmarking-and-capstone/02-apply-optimization-measure-improvement/tests.py
"""

import sys
from pathlib import Path

import numpy as np

sys.path.insert(0, str(Path(__file__).resolve().parents[3]))
from _load import load_solution  # noqa: E402

_module = load_solution(f"10-rl-alignment/04-benchmarking-and-capstone/{Path(__file__).resolve().parent.name}")
optimized_matmul = _module.optimized_matmul
verify_optimization_correctness = _module.verify_optimization_correctness
benchmark_optimization = _module.benchmark_optimization
matmul_from_scratch = _module.matmul_from_scratch


def _random_matrices(seed, n=40):
    rng = np.random.default_rng(seed)
    return rng.normal(size=(n, n)), rng.normal(size=(n, n))


# --- Basic correctness (the two the "Run" button samples) -----------------


def test_01_optimized_matmul_matches_the_baseline():
    a, b = _random_matrices(0)
    assert np.allclose(optimized_matmul(a, b), matmul_from_scratch(a, b))


def test_02_optimization_is_verified_correct():
    a, b = _random_matrices(1)
    assert verify_optimization_correctness(a, b) is True


# --- General-case coverage --------------------------------------------


def test_03_optimized_matmul_matches_direct_numpy_matmul():
    a, b = _random_matrices(2)
    assert np.allclose(optimized_matmul(a, b), a @ b)


def test_04_benchmark_reports_a_real_speedup():
    a, b = _random_matrices(3)
    result = benchmark_optimization(a, b, num_runs=3)
    # Conservative threshold: this specific optimization (vectorized
    # matmul vs. a doubly-nested Python loop) is reliably orders of
    # magnitude faster, so even generous CI-noise headroom stays well
    # clear of any risk of flakiness.
    assert result["speedup_factor"] > 5.0


def test_05_benchmark_result_includes_correctness_verification():
    a, b = _random_matrices(4)
    result = benchmark_optimization(a, b, num_runs=3)
    assert result["correctness_verified"] is True


# --- Parameter handling -------------------------------------------------


def test_06_benchmark_result_has_baseline_and_optimized_stats():
    a, b = _random_matrices(5)
    result = benchmark_optimization(a, b, num_runs=3)
    assert set(result["baseline"].keys()) == {"mean", "median", "min", "max", "std"}
    assert set(result["optimized"].keys()) == {"mean", "median", "min", "max", "std"}


def test_07_larger_matrices_still_produce_a_real_speedup():
    a, b = _random_matrices(6, n=50)
    result = benchmark_optimization(a, b, num_runs=2)
    assert result["speedup_factor"] > 5.0


# --- Edge cases ---------------------------------------------------------


def test_08_correctness_check_detects_a_genuine_mismatch():
    a, b = _random_matrices(7)
    wrong_result = matmul_from_scratch(a, b) + 1.0  # deliberately broken
    assert not np.allclose(wrong_result, optimized_matmul(a, b))


def test_09_small_matrices_still_verify_correct():
    a, b = _random_matrices(8, n=3)
    assert verify_optimization_correctness(a, b) is True


# --- Independent correctness oracle -----------------------------------


def test_10_speedup_factor_computed_from_the_actual_measured_stats():
    # Directly targets a mutant that hardcodes or fabricates a
    # plausible-looking speedup number instead of deriving it from the
    # actual measured baseline/optimized statistics.
    a, b = _random_matrices(9)
    result = benchmark_optimization(a, b, num_runs=3)
    expected = result["baseline"]["median"] / result["optimized"]["median"]
    assert np.isclose(result["speedup_factor"], expected)
