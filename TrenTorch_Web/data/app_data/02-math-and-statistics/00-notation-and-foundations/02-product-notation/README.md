---
name: math-product-notation
title: 'Product Notation: expanding and evaluating ∏'
tags: [notation, foundations]
difficulty: Beginner
---

## Statement

### The problem, from first principles

`01-summation-notation`'s `Σ` accumulates by adding. `∏` (capital pi) is the exact same accumulation pattern, just multiplying instead — and it shows up wherever probabilities of independent events combine (the likelihood of a whole dataset is a product of per-example probabilities) or wherever a count is built up multiplicatively (a factorial, covered next, is itself a `∏`).

### From theory to code

Implement `product(f, lo, hi)`, computing `∏_{i=lo}^{hi} f(i)` — call `f` once per integer `i` from `lo` to `hi` **inclusive**, and multiply the results together. The signature and docstring are already in the editor.

### Constraints

- `lo` and `hi` are integers; `hi` may be less than `lo`, in which case the product is empty (the standard mathematical convention: an empty product is `1`, not `0` — multiplying by nothing should leave a value unchanged, exactly like adding nothing leaves a sum unchanged at `0`).
- `f` takes a single integer and returns a number (int or float).

### Hints

<details>
<summary>Hint 1</summary>

Structurally identical to `01-summation-notation`'s loop — only the accumulator's starting value (`1` instead of `0`) and the combining operation (`*=` instead of `+=`) differ.

</details>

<details>
<summary>Hint 2</summary>

Starting the accumulator at `1` is exactly what makes the empty-range case correctly return `1` with no special-cased branch, the same way starting at `0` did for summation's empty case.

</details>

## Theory

### The simple version

`∏_{i=1}^{4} i` reads as "multiply `i`, for every integer `i` from `1` to `4`": `1 × 2 × 3 × 4 = 24`. Same loop-and-accumulate shape as `Σ`, with multiplication in place of addition.

### The formula

$$
\prod_{i=\text{lo}}^{\text{hi}} f(i) = f(\text{lo}) \times f(\text{lo}+1) \times \cdots \times f(\text{hi})
$$

- `i` — the index variable, exactly as in `Σ`.
- `lo`, `hi` — the range's bounds, both inclusive.
- `f(i)` — the factor contributed by each index, multiplied into the running product.

### Why the empty case is 1, not 0

An empty sum should leave a running total unaffected if nothing is added — that identity value is `0`. An empty product should leave a running total unaffected if nothing is multiplied in — that identity value is `1`, since multiplying by `0` would collapse everything to `0` regardless of what came before. This same "identity element" idea reappears constantly: the identity matrix (`02-linear-algebra`'s `Matrix inverse` topic) plays the same role for matrix multiplication that `1` plays here for ordinary multiplication.

### Where this shows up

- **Factorial** (next question): `n! = ∏_{i=1}^{n} i`.
- **Likelihood of independent observations**: if each data point's probability is `p(x_i)`, and the points are independent, the whole dataset's likelihood is `∏_i p(x_i)` — this exact product is why Maximum Likelihood Estimation (later in this track) almost always works with its **logarithm** instead, turning a product of many small numbers (which underflows to `0` in floating point) into a sum via `log(∏ p(x_i)) = Σ log p(x_i)`.

### How code actually implements this

`math.prod(values)` (Python's standard library) and `np.prod(arr)` both compute this same accumulation in one call, exactly analogous to `sum()`/`.sum()` for `Σ`.

## Explanation

`product` starts `total = 1` and loops `i` over `range(lo, hi + 1)`, multiplying `f(i)` into `total` each iteration — identical structure to `summation`, with the accumulator's identity value and combining operator swapped to match multiplication instead of addition. When `hi < lo`, the loop body never runs and `total` stays at its initial value `1`, correctly matching the empty-product convention with no extra branch.
