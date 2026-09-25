---
name: numpy-default-rng
title: 'The Modern Random API: default_rng'
tags: [numpy-random]
difficulty: Beginner
---

## Statement

Implement functions that create random number generators using `np.random.default_rng()` and confirm each generator is an independent object with its own state.

## Theory

The **legacy API** (`np.random.seed`, `np.random.rand`, ...) reads and mutates a single global generator state shared by the entire program — any code calling `np.random.*` advances the same hidden state.

The **modern API** replaces this with an explicit object:

```python
rng = np.random.default_rng(42)
rng.random(3)     # draws from THIS Generator's own state
```

A `Generator` is a normal Python object: it can be stored, passed as an argument, and is mutable — calling a method on it changes its state in place. Two variables pointing at the same `Generator` share state; two separately created `Generator` objects do not.

## Explanation

`create_rng` returns `np.random.default_rng(seed)` directly, never touching the legacy API. `make_independent_rngs` creates two separate `Generator` objects from `seed_a` and `seed_b` — since each owns its own state, drawing from one never affects the other. `draw` calls `rng.random(n)`, which both returns values and advances `rng`'s state as a side effect.
