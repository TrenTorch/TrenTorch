---
name: numpy-seeding-and-reproducibility
title: Seeding and Reproducibility
tags: [numpy-random]
difficulty: Intermediate
---

## Statement

Implement functions demonstrating what a seed controls, how a generator's state advances with each draw, and how passing a generator into a function mutates the caller's generator.

## Theory

The same seed always produces the same initial state, and therefore the same sequence of values:

```python
np.random.default_rng(7).random(3) == np.random.default_rng(7).random(3)
```

**Draws consume the sequence in order.** Calling `rng.random(3)` twice gives two _different_ arrays — the second continues where the first stopped. Drawing 5 then 3 gives the same values as drawing 8 in one call.

**Mutation through a function argument.** A `Generator` passed into a function is the same object — mutations (draws) made inside are visible to the caller, exactly like any other mutable object in Python.

```python
def take_two(rng):
    return rng.random(2)     # mutates rng's state in place

rng = np.random.default_rng(7)
take_two(rng)                  # caller's rng has advanced by 2 draws
```

## Explanation

`reproducible_draw` creates a fresh `Generator` from `seed` each call and draws `n` values — deterministic given the same arguments. `draw_twice` creates **one** generator and draws twice in sequence, returning both arrays (necessarily different, since the second continues the sequence). `same_seed_same_output` creates two separate generators from the same seed and compares their draws with `np.array_equal`. `skip_then_draw` discards `skip` values from the given `rng` (e.g. `rng.random(skip)`, discarding the result) then returns the next `n` — operating on the passed-in `rng` directly, so the caller's generator ends up advanced by `skip + n`.
