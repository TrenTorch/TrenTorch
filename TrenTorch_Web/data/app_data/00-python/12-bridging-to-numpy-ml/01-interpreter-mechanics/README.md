---
name: python-numpy-bridge-interpreter-mechanics
title: "Why Plain Python Loops Are Slow: Interpreter Mechanics"
tags: [python-numpy-bridge]
difficulty: Intermediate
---

## Statement

Implement a plain-loop dot product and small cost models that compare interpreted per-element work with vectorized execution and list storage with typed-array storage.

## Theory

For every element of `c.append(a[i] + b[i])`, the interpreter: advances the loop, looks up `a[i]` and `b[i]` (following addresses), finds and calls `__add__` based on the objects' types, **allocates a new result object**, then looks up and calls `append`. The arithmetic itself is a tiny fraction of this — the rest is dispatch, allocation, and indirection.

**Storage.** A list stores addresses; each number is a separate object (~28 bytes for a small int) plus 8 bytes for the list slot: $\text{bytes}_{\text{list}} \approx n \cdot (8 + 28)$. A typed array holds raw numbers of one type contiguously, with no per-element object: $\text{bytes}_{\text{array}} = n \cdot \text{itemsize}$.

**Vectorization.** `c = a + b` on arrays runs a single call whose compiled loop knows the type once and never allocates per element. A simple cost model, with $p$ the per-iteration Python-loop cost, $e$ the per-element compiled cost, and $c$ the fixed per-call overhead:

$$T_{\text{loop}}(n) = n \cdot p \qquad T_{\text{vec}}(n) = c + n \cdot e$$

The break-even size satisfies $n \cdot p = c + n \cdot e$, so $n = \dfrac{c}{p - e}$ — vectorization only ever wins for large $n$ when $e < p$.

A list comprehension is still an interpreted loop — it removes some bookkeeping but still dispatches and allocates per element; the speedup of vectorization comes from moving the loop out of the interpreter entirely, not from different syntax.

**Where this matters later.** Every NumPy/PyTorch track relies on this: operate on whole arrays, avoid Python-level per-element loops.

## Explanation

`break_even_n` computes the exact real-valued threshold `call_overhead / (per_iteration_cost - per_element_cost)` and rounds up with `math.ceil`, since $n$ must be a whole count of elements and any $n$ below the exact threshold fails the inequality — rounding down could return an $n$ that doesn't actually satisfy it. It returns `None` when `per_element_cost >= per_iteration_cost`, since a division by a non-positive number there wouldn't mean vectorization never wins for large $n$, it would mean the formula's premise breaks. `list_of_ints_bytes` and `typed_array_bytes` are direct multiplications from the theory's own byte formulas, with `n <= 0` guarded to `0` since a non-positive count of elements has no memory cost.
