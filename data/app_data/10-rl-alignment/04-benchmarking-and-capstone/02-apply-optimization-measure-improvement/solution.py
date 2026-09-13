import sys
from pathlib import Path

import numpy as np

sys.path.insert(0, str(Path(__file__).resolve().parents[3]))
from _load import load_solution  # noqa: E402

matmul_from_scratch = load_solution("00-math-and-statistics/01-linear-algebra/03-matrix-multiplication").matmul_from_scratch
time_function = load_solution("10-rl-alignment/04-benchmarking-and-capstone/01-benchmark-harness").time_function
benchmark_statistics = load_solution(
    "10-rl-alignment/04-benchmarking-and-capstone/01-benchmark-harness"
).benchmark_statistics


def optimized_matmul(a: np.ndarray, b: np.ndarray) -> np.ndarray:
    return a @ b


def verify_optimization_correctness(a: np.ndarray, b: np.ndarray) -> bool:
    baseline_result = matmul_from_scratch(a, b)
    optimized_result = optimized_matmul(a, b)
    return bool(np.allclose(baseline_result, optimized_result))


def benchmark_optimization(a: np.ndarray, b: np.ndarray, num_runs: int = 5) -> dict:
    baseline_times = time_function(lambda: matmul_from_scratch(a, b), num_runs=num_runs)
    optimized_times = time_function(lambda: optimized_matmul(a, b), num_runs=num_runs)
    baseline_stats = benchmark_statistics(baseline_times)
    optimized_stats = benchmark_statistics(optimized_times)
    return {
        "baseline": baseline_stats,
        "optimized": optimized_stats,
        "speedup_factor": baseline_stats["median"] / optimized_stats["median"],
        "correctness_verified": verify_optimization_correctness(a, b),
    }
