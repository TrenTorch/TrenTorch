---
name: numpy-measuring-vectorized-vs-loop-performance
title: Measuring Vectorized vs Loop-Based Performance
tags: [numpy-memory]
difficulty: Intermediate
---

## Statement

Implement a loop-based and a vectorized version of the same computation, a timing helper, and a benchmark that measures how much faster the vectorized version is.

## Theory

**Why the loop is slow.** Every iteration of a plain Python `for` loop runs through the interpreter, wrapping each element into a new object before Python can use it.

**Why the vectorized version is fast.** A vectorized operation is a single call — the loop over all elements runs in compiled code over one contiguous buffer.

**Timing:**

```python
import time
start = time.perf_counter()
result = some_function(data)
elapsed = time.perf_counter() - start
```

A single measurement is noisy; the standard approach is to repeat and take the **minimum**, since noise can only add time.

**Speedup** is $t_{\text{loop}} / t_{\text{vectorized}}$.

```python
def loop_sum_of_squares(values):
    total = 0
    for v in values:
        total += v * v
    return total

def vectorized_sum_of_squares(arr):
    return (arr * arr).sum()
```

## Explanation

`loop_sum_of_squares` accumulates with a Python `for` loop. `vectorized_sum_of_squares` is `(arr * arr).sum()`. `best_time` calls `func(*args)` `repeats` times, timing each with `time.perf_counter()`, and returns `min(...)` of the recorded durations. `benchmark_sum_of_squares` builds the same values as a list and as `np.arange(n)`, times both with `best_time`, and reports both durations, their ratio, and whether the two results agree.
