---
name: numpy-vectorized-vs-loop-speed
title: Why Vectorized Operations Are Faster Than a Loop
tags: [numpy-core]
difficulty: Intermediate
---

## Statement

Implement the same computation two ways — an explicit Python loop and a vectorized NumPy expression — and measure the actual time difference directly.

## Theory

Every Python-level loop iteration carries real overhead: variable lookups, type checks, and dynamic dispatch, per element, no matter how simple the computation.

A vectorized NumPy operation avoids this entirely. Because every element in an ndarray's buffer is a fixed-size type, NumPy hands the whole operation to a single pre-compiled C loop — type checking, lookup, and dispatch happen once for the whole array, not once per element.

```python
arr = np.arange(1_000_000)
result_loop = np.empty_like(arr)
for i in range(len(arr)):
    result_loop[i] = arr[i] * 2     # slow — per-element Python overhead

result_vectorized = arr * 2         # fast — single C loop
```

For large arrays, vectorized is routinely tens to hundreds of times faster, with no change to the actual math.

**The practical rule:** whenever an operation applies uniformly across an array, express it that way rather than writing a Python loop.

## Explanation

`multiply_with_loop` iterates with a Python `for` loop, writing `arr[i] * factor` into a result array. `multiply_vectorized` is the single expression `arr * factor`. `time_both_approaches` times each with `time.perf_counter()` around the call, returning both results and both durations plus a direct `<` comparison of the two timings.
