---
name: numpy-uniform-and-integer-arrays
title: Uniform and Integer Random Arrays
tags: [numpy-random]
difficulty: Beginner
---

## Statement

Implement functions that generate arrays of uniformly distributed floats and random integers with a specified shape and range, paying attention to which interval endpoints are included.

## Theory

Every `Generator` method accepts a **`size`** argument, working like Module 1's `shape`: an integer gives 1D, a tuple gives multi-dimensional.

**Uniform floats.** `rng.random(size)` returns floats over $[0, 1)$. `rng.uniform(low, high, size)` spreads them over $[\text{low}, \text{high})$ instead.

```python
rng.uniform(-1.0, 1.0, 5)     # 5 values in [-1, 1)
```

**Random integers.** `rng.integers(low, high, size)` returns integers from $[\text{low}, \text{high})$ — upper bound **exclusive**. Passing `endpoint=True` makes it inclusive: $[\text{low}, \text{high}]$.

```python
rng.integers(0, 10, size=5)                 # 0..9
rng.integers(1, 6, size=5, endpoint=True)   # 1..6 (a six-sided die)
```

Confusing exclusive vs inclusive is a classic off-by-one: `integers(1, 6)` alone never produces a `6`.

## Explanation

`uniform_array` is `rng.uniform(low, high, shape)`. `random_integers` is `rng.integers(low, high, size=shape)`, exclusive upper bound. `roll_dice` is `rng.integers(1, sides, size=n_dice, endpoint=True)` — `endpoint=True` is exactly what makes the top face (`sides`) reachable.
