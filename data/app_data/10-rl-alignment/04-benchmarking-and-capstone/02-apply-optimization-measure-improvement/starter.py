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
    """
    The "one optimization" applied to `math-matrix-multiplication`'s
    from-scratch, doubly-nested-loop `matmul_from_scratch`: just use
    NumPy's own vectorized `@` operator instead.
    """
    # TODO: return a @ b
    pass


def verify_optimization_correctness(a: np.ndarray, b: np.ndarray) -> bool:
    """
    An optimization that's FAST but WRONG is worthless -- always
    verify the optimized version's output actually matches the
    baseline's before trusting any speedup number.
    """
    # TODO: compare matmul_from_scratch(a, b) against
    # optimized_matmul(a, b) with np.allclose, return the bool result.
    pass


def benchmark_optimization(a: np.ndarray, b: np.ndarray, num_runs: int = 5) -> dict:
    """
    Runs 01-benchmark-harness's time_function on BOTH the baseline and
    the optimized implementation (same inputs), summarizes each with
    benchmark_statistics, and reports the real, measured speedup
    (baseline median time / optimized median time) alongside a
    correctness check.
    """
    # TODO: time_function each implementation (wrap each call in a
    # lambda closing over a, b), get benchmark_statistics for each,
    # then return a dict with keys "baseline", "optimized",
    # "speedup_factor" (baseline median / optimized median), and
    # "correctness_verified".
    pass
