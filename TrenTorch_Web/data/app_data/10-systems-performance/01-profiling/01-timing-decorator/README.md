---
name: systems-perf-timing-decorator
title: Timing Decorator
tags: [mlops, profiling]
difficulty: Beginner
---

## Statement

### The problem, from first principles

"Is this faster?" is one of the most common questions in ML systems work — is this kernel fusion actually helping, does this batch size change hurt throughput, is the new data loader really the bottleneck. Answering it requires measuring, not guessing, and measuring the same way every time a function is called quickly becomes tedious to write by hand at every call site.

### From theory to code

Implement `timed(func)`, a decorator that wraps any function so that calling the wrapped version runs the original function and returns `(result, elapsed_seconds)` instead of just `result` — one reusable measurement tool instead of hand-rolled timing code scattered everywhere.

### Constraints

- `timed(func)` returns a new callable with the same calling convention as `func` (same positional and keyword arguments).
- The wrapped callable returns a 2-tuple: `(original_result, elapsed_seconds)`.
- `elapsed_seconds` is measured using a monotonic, high-resolution clock — never negative, never affected by system clock changes.
- The wrapped function preserves `func`'s `__name__` and docstring (via `functools.wraps`).

### Hints

Open one at a time. Each gives away a little more than the last.

<details>
<summary>Hint 1</summary>

`time.perf_counter()` is Python's monotonic, high-resolution timer — call it once immediately before running `func`, and once immediately after, then subtract.

</details>

<details>
<summary>Hint 2</summary>

`@wraps(func)` from `functools`, applied to your inner wrapper function, is what makes the wrapped function keep `func`'s real `__name__` and docstring instead of showing `wrapper` everywhere.

</details>

## Theory

### The simple version

Think of `timed` as handing a stopwatch to whatever function it wraps: the function does its normal job, completely unaware anything is different, and the decorator quietly starts the stopwatch right before and stops it right after, then hands back both the function's real answer and how long it took to get there.

### The formula

```text
start   = perf_counter()
result  = func(*args, **kwargs)
elapsed = perf_counter() - start
return (result, elapsed)
```

### How PyTorch actually implements this

Context only, untested by your submission: real PyTorch profiling goes considerably further than a wall-clock decorator — `torch.profiler.profile` and `torch.cuda.Event`-based timing account for GPU kernel launches being asynchronous (a naive `time.perf_counter()` around a GPU op would measure how long it took to _launch_ the kernel, not how long the kernel actually ran, unless a synchronization point is inserted first). For CPU-only NumPy code like this exercise's, `perf_counter()` around the call is exactly correct and needs no such synchronization.

## Explanation

`timed` defines an inner `wrapper(*args, **kwargs)` function, decorated with `@wraps(func)` so it inherits `func`'s `__name__` and docstring rather than showing up as a generic `wrapper` everywhere it's introspected. Inside, `time.perf_counter()` is read immediately before calling `func(*args, **kwargs)` and immediately after, and the difference is the elapsed wall-clock time for exactly that call — `*args, **kwargs` in both the wrapper's signature and the inner call is what lets `timed` wrap a function of any signature, not just a fixed one.
