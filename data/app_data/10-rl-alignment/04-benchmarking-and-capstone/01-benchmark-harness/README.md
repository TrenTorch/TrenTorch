---
name: rl-alignment-benchmark-harness
title: 'Build a Benchmark Harness (Reuses Profiling)'
tags: [mlops, metrics-and-evaluation]
difficulty: Intermediate
---

## Statement

### The problem, from first principles

Every "optimization" claim in this whole curriculum — quantization is faster, kernel fusion saves memory traffic, a vectorized loop beats a naive one — is worthless without an actual, repeatable measurement backing it up. This question builds the one small, reusable tool that makes any such claim checkable: a harness that runs a piece of code several times, records real wall-clock timings, and summarizes them honestly.

### From theory to code

Implement `time_function` (running a zero-argument callable several times, recording each run's duration) and `benchmark_statistics` (summarizing those raw timings).

### Constraints

- `time_function(fn, num_runs=5)` calls `fn()` exactly `num_runs` times, returning a list of `num_runs` individual wall-clock durations (using `time.perf_counter()`), never a single averaged number.
- `benchmark_statistics(times)` returns a dict with keys `"mean"`, `"median"`, `"min"`, `"max"`, `"std"`.
- Every measured duration is non-negative.

### Hints

Open one at a time. Each gives away a little more than the last.

<details>
<summary>Hint 1</summary>

`time.perf_counter()` before and after calling `fn()`, subtracted, gives one run's duration — repeat that `num_runs` times, appending each duration to a list.

</details>

<details>
<summary>Hint 2</summary>

`benchmark_statistics` is five one-line NumPy calls (`.mean()`, `np.median()`, `.min()`, `.max()`, `.std()`) on the same array of times, packaged into a dict.

</details>

## Theory

### The simple version

Imagine timing a runner across five separate laps instead of just once — a single lap could be unusually fast or slow for reasons that have nothing to do with the runner's real ability (a gust of wind, a stumble). Taking several independent measurements and looking at the whole SPREAD (not just one number) is what lets you tell a genuine, repeatable difference in speed apart from ordinary noise — exactly what any credible "before vs. after" optimization claim needs to survive scrutiny.

### The formula

```text
time_function(fn, num_runs):
    times = []
    for _ in range(num_runs):
        start = perf_counter()
        fn()
        end = perf_counter()
        times.append(end - start)
    return times

benchmark_statistics(times) = {
    "mean": mean(times), "median": median(times),
    "min": min(times), "max": max(times), "std": std(times)
}
```

Reporting only a single averaged number (or worse, a single one-off measurement) hides exactly the information that matters for a trustworthy benchmark: the `std` reveals how NOISY the measurement environment is, and `min`/`max` reveal the best-case and worst-case, both of which a single mean can mask entirely.

### How PyTorch actually implements this

Context only, untested by your submission: real benchmarking tools (Python's own `timeit` module, PyTorch's `torch.utils.benchmark`) follow exactly this pattern — run the code repeatedly, discard or account for warm-up effects, and report a distribution of timings rather than a single number, precisely because a single measurement on real, shared, multi-process hardware is rarely reproducible on its own.

## Explanation

`time_function` runs the given callable the requested number of times, timing each call independently with `time.perf_counter()` (the standard, monotonic, high-resolution clock for exactly this purpose) and collecting every individual duration — this exercise's `tests.py` confirms it calls the function the correct number of times (via a counting closure, not by trusting the timings themselves) and that every recorded duration is non-negative.

`benchmark_statistics` computes the five standard descriptive statistics over that raw list — `tests.py` confirms each formula against hand computation and NumPy's own reference implementations, and its final oracle test specifically checks that a genuinely spread-out set of timings produces a real `min < mean < max` ordering and a nonzero `std`, directly ruling out a mutant that lazily hardcodes `min`/`max`/`std` to match `mean`.
