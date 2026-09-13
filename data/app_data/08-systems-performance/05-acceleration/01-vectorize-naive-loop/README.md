---
name: systems-perf-vectorize-naive-loop
title: Vectorize a Naive Python Loop into NumPy Ops, Before/After Speed Comparison
tags: [mlops, acceleration]
difficulty: Beginner
---

## Statement

### The problem, from first principles

Every operation in this curriculum's classical-ML and deep-learning tracks was implemented as a single vectorized NumPy expression, deliberately avoiding Python-level loops over individual elements — this question makes the reason for that convention explicit and measurable, rather than assumed.

### From theory to code

Implement `naive_dot_product(a, b)` (a plain Python loop over two lists), `vectorized_dot_product(a, b)` (the identical computation as one NumPy call), and `compare_speed(a, b)`, which runs both on the same data and reports both the results and the actual measured timings.

### Constraints

- `naive_dot_product`: takes plain Python lists, returns a `float`.
- `vectorized_dot_product`: takes NumPy arrays, returns a `float`.
- `compare_speed`: takes NumPy arrays, returns a dict with `naive_result`, `vectorized_result`, `naive_time`, `vectorized_time`, `speedup` (`naive_time / vectorized_time`).
- `compare_speed` internally converts its array inputs to lists for `naive_dot_product` — it doesn't change what's being measured, only which representation each implementation actually expects.

### Hints

Open one at a time. Each gives away a little more than the last.

<details>
<summary>Hint 1</summary>

`naive_dot_product` is the dot product exactly as anyone would first write it without knowing NumPy exists: a loop, one multiplication and one addition per pair of elements.

</details>

<details>
<summary>Hint 2</summary>

`np.dot(a, b)` does the _entire_ dot product in one call, dispatching to a highly-optimized (often BLAS-backed) routine — there's no loop for Python to interpret one instruction at a time.

</details>

## Theory

### The simple version

A Python `for` loop pays a real, fixed overhead cost _per iteration_ just for being interpreted Python bytecode — before any actual multiplication or addition even happens. A single NumPy call pays that interpreter overhead exactly once, then hands the entire computation to compiled, optimized C (or Fortran, via BLAS) code that runs the whole loop internally, at native speed, with none of Python's per-iteration tax. The more elements involved, the more that per-iteration overhead adds up, and the more dramatic the vectorized version's advantage becomes.

### The formula

```text
naive_dot_product(a, b)      = sum(x * y for x, y in zip(a, b))     # one Python-level iteration per pair
vectorized_dot_product(a, b) = np.dot(a, b)                          # one call, computed natively
speedup                      = naive_time / vectorized_time
```

### How PyTorch actually implements this

Context only, untested by your submission: this is exactly why every tensor operation in this curriculum (and in real PyTorch) is written as a single vectorized call rather than a Python loop over elements — `torch.Tensor` operations dispatch to compiled C++/CUDA kernels the same way NumPy dispatches to BLAS, and a Python-level loop over individual tensor elements would be catastrophically slower on a GPU specifically, since it would serialize what the hardware is built to do in parallel across thousands of cores at once.

## Explanation

`naive_dot_product` iterates `zip(a, b)` in plain Python, accumulating `x * y` into `total` one pair at a time — every single multiplication and addition, plus the loop machinery itself, runs through Python's interpreter.

`vectorized_dot_product` is `np.dot(a, b)` directly — the entire computation happens inside NumPy's compiled implementation, with Python only paying its interpreter overhead once, for the single function call, regardless of how large `a`/`b` are.

`compare_speed` converts `a`/`b` to plain lists once (for `naive_dot_product`'s sake, since it expects lists rather than arrays), times each implementation's actual call with `time.perf_counter()` immediately before and after, and packages both results and both timings — including `speedup`, the direct, measured ratio — into one dict, so the vectorization's benefit is demonstrated with a real number rather than just claimed.
