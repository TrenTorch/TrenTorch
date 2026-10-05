---
name: numpy-generators-seeding
title: 'Generators & Seeding'
tags: [numpy-random]
difficulty: Intermediate
---

## Statement

Implement functions that create independent random number generators, demonstrating what a seed controls, how a generator's state advances with each draw and how passing a generator into a function makes results reproducible.

## Theory

### Random generators

The **legacy API** (`np.random.seed`, `np.random.rand`, ...) reads and mutates a single global generator state shared by the entire program, any code calling `np.random.*` advances the same hidden state.

The **modern API** replaces this with an explicit object:

```python
rng = np.random.default_rng(42)
rng.random(3)     # draws from THIS Generator's own state
```

A `Generator` is a normal Python object: it can be stored, passed as an argument, and is mutable, calling a method on it changes its state in place. Two variables pointing at the same `Generator` share state; two separately created `Generator` objects do not.

### Seeding & reproducibility

The same seed always produces the same initial state, and therefore the same sequence of values:

```python
np.random.default_rng(7).random(3) == np.random.default_rng(7).random(3)
```

**Draws consume the sequence in order.** Calling `rng.random(3)` twice gives two _different_ arrays, the second continues where the first stopped. Drawing 5 then 3 gives the same values as drawing 8 in one call.

**Mutation through a function argument.** A `Generator` passed into a function is the same object, mutations (draws) made inside are visible to the caller, exactly like any other mutable object in Python.

```python
def take_two(rng):
    return rng.random(2)     # mutates rng's state in place

rng = np.random.default_rng(7)
take_two(rng)                  # caller's rng has advanced by 2 draws
```

## Explanation

`create_rng` returns `np.random.default_rng(seed)` directly, never touching the legacy API. `make_independent_rngs` creates two separate `Generator` objects from `seed_a` and `seed_b`, since each owns its own state, drawing from one never affects the other. `draw` calls `rng.random(n)`, which both returns values and advances `rng`'s state as a side effect.

`reproducible_draw` creates a fresh `Generator` from `seed` each call and draws `n` values, deterministic given the same arguments. `draw_twice` creates **one** generator and draws twice in sequence, returning both arrays (necessarily different, since the second continues the sequence). `same_seed_same_output` creates two separate generators from the same seed and compares their draws with `np.array_equal`. `skip_then_draw` discards `skip` values from the given `rng` (e.g. `rng.random(skip)`, discarding the result) then returns the next `n`, operating on the passed-in `rng` directly, so the caller's generator ends up advanced by `skip + n`.
