---
name: numpy-arange-and-linspace
title: arange and linspace
tags: [numpy-core]
difficulty: Beginner
---

## Statement

Implement functions using `np.arange` and `np.linspace` to generate numeric sequences, and a function that demonstrates precisely how the two differ.

## Theory

`np.arange(start, stop, step)` generates values starting at `start`, increasing by `step`, stopping **before** `stop` — `stop` itself is never included. This mirrors Python's `range()`, but supports non-integer steps.

```python
np.arange(0, 10, 2)     # [0, 2, 4, 6, 8] — stops before 10
np.arange(0, 1, 0.25)   # [0.0, 0.25, 0.5, 0.75]
```

`np.linspace(start, stop, num)` generates exactly `num` evenly-spaced values, and — unlike `arange` — **includes** `stop` as the final value by default.

```python
np.linspace(0, 10, 5)    # [0.0, 2.5, 5.0, 7.5, 10.0] — 5 values, endpoint included
```

**Core distinction:** `arange` is controlled by step size and excludes the endpoint; `linspace` is controlled by count and includes the endpoint by default.

## Explanation

`make_range` and `make_evenly_spaced` are direct one-line calls to `np.arange` and `np.linspace` respectively. `compare_arange_linspace` chains them: build the `arange` array, take its length with `len(...)`, then build a `linspace` array with that same length as `num` over the same start/stop — then check membership of `stop` in each with the `in` operator (works fine for a small ndarray).
