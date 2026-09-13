---
name: rl-alignment-apply-optimization-measure-improvement
title: 'Apply One Optimization, Measure Real Improvement'
tags: [mlops, metrics-and-evaluation]
difficulty: Intermediate
---

## Statement

### The problem, from first principles

`01-benchmark-harness` built the measurement tool — this question puts it to real use: take a genuine baseline implementation (`math-matrix-multiplication`'s from-scratch, doubly-nested-loop matmul), apply ONE concrete optimization (swap in NumPy's vectorized `@` operator), and measure whether it's ACTUALLY faster — while never trusting a speedup number until the optimized version's OUTPUT has also been checked against the baseline.

### From theory to code

Implement `optimized_matmul` (the optimization itself), `verify_optimization_correctness` (checking the optimization didn't change the answer), and `benchmark_optimization`, tying both the speed measurement and the correctness check together into one result.

### Constraints

- `optimized_matmul(a, b)` returns `a @ b`.
- `verify_optimization_correctness(a, b)` returns `True` exactly when `matmul_from_scratch(a, b)` and `optimized_matmul(a, b)` agree (via `np.allclose`).
- `benchmark_optimization(a, b, num_runs=5)` times both implementations with `01-benchmark-harness`'s `time_function`, and returns a dict with `"baseline"`/`"optimized"` statistics, a `"speedup_factor"` (baseline median / optimized median), and `"correctness_verified"`.

### Hints

Open one at a time. Each gives away a little more than the last.

<details>
<summary>Hint 1</summary>

Use MEDIAN (not mean) timing for `speedup_factor` — a median is more robust to the occasional unusually slow measurement (a stray OS scheduling hiccup) than a mean is.

</details>

<details>
<summary>Hint 2</summary>

`benchmark_optimization` should call `time_function(lambda: matmul_from_scratch(a, b), num_runs=num_runs)` and `time_function(lambda: optimized_matmul(a, b), num_runs=num_runs)` — wrapping each call in a lambda is what lets `time_function`'s zero-argument-callable contract work with functions that actually need arguments.

</details>

## Theory

### The simple version

Imagine claiming a new delivery route is "way faster" without ever checking it still delivers to the RIGHT address — speed without correctness isn't an optimization, it's just a different (broken) program that happens to run quickly. This exercise insists on both halves of the claim at once: `matmul_from_scratch`'s doubly-nested Python loop computes the exact right answer, slowly; `optimized_matmul` needs to compute the SAME right answer, measurably faster — and only a result that satisfies both counts as a real optimization.

### The formula

```text
optimized_matmul(a, b) = a @ b

verify_optimization_correctness(a, b) = np.allclose(matmul_from_scratch(a, b), optimized_matmul(a, b))

benchmark_optimization(a, b, num_runs):
    baseline_stats  = benchmark_statistics(time_function(lambda: matmul_from_scratch(a, b), num_runs))
    optimized_stats = benchmark_statistics(time_function(lambda: optimized_matmul(a, b), num_runs))
    speedup_factor  = baseline_stats.median / optimized_stats.median
```

For genuinely sized matrices, this specific optimization isn't a marginal improvement — a doubly-nested Python loop calling into NumPy once per output element pays enormous per-call overhead compared to NumPy's own fully-vectorized `@`, which is exactly why this exercise's speedup threshold can be set generously (`> 5x`) with zero real risk of flakiness, unlike `06-kernels`' NumPy-timing pitfalls, where the effects being measured were genuinely too small and subtle for wall-clock timing to reliably demonstrate.

### How PyTorch actually implements this

Context only, untested by your submission: this exact "measure a real baseline, apply one targeted change, re-measure, and verify correctness before trusting the speedup" workflow is the standard discipline behind any legitimate performance optimization claim in real ML systems work — profiling tools (`08-systems-performance`'s `05-profiling` track) identify WHERE time is spent, and this benchmarking discipline confirms whether a proposed fix actually helped, and by how much, rather than trusting intuition alone.

## Explanation

`optimized_matmul` is a one-line call to NumPy's `@`, the fully-vectorized alternative to `matmul_from_scratch`'s Python-level double loop.

`verify_optimization_correctness` runs both implementations on the SAME inputs and compares their outputs directly — `tests.py` confirms it correctly returns `True` for the real optimized implementation, and also confirms it correctly detects a deliberately broken "optimization" whose output doesn't match, proving the check does real comparison work rather than trivially passing.

`benchmark_optimization` ties the speed and correctness measurements together into one result — `tests.py` verifies the reported speedup is genuinely large (reflecting the real, dramatic gap between a Python-loop implementation and vectorized NumPy) and, via its final oracle test, that `speedup_factor` is actually DERIVED from the reported baseline/optimized statistics rather than a separately hardcoded number, directly ruling out a mutant that fabricates a plausible-looking speedup independent of what was actually measured.
