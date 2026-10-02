---
name: math-summation-notation
title: 'Summation Notation: expanding and evaluating Σ'
tags: [notation, foundations]
difficulty: Beginner
---

## Statement

### The problem, from first principles

Every other track on this site writes formulas using `Σ` (sigma) without ever teaching what it means — a loss function's `Σ_i (y_i - ŷ_i)²`, entropy's `-Σ_x p(x) log p(x)`, a dot product's `Σ_i a_i b_i`. All of them are the exact same idea: "add up a sequence of values, one per index, over a specified range." This question makes that idea concrete before it shows up disguised inside a bigger formula.

### From theory to code

`Σ` is nothing more than a `for` loop that accumulates a running total. Implement `summation(f, lo, hi)`, computing `Σ_{i=lo}^{hi} f(i)` — call `f` once per integer `i` from `lo` to `hi` **inclusive**, and add up the results. The signature and docstring are already in the editor.

### Constraints

- `lo` and `hi` are integers; `hi` may be less than `lo`, in which case the sum is empty (the standard mathematical convention: an empty sum is `0`).
- `f` takes a single integer and returns a number (int or float).
- Do not use `sum()` with a generator that secretly hides the loop from yourself — write the accumulation explicitly, since the point is to see the mechanics `Σ` is standing in for.

### Hints

<details>
<summary>Hint 1</summary>

`range(lo, hi + 1)` — `hi` is inclusive in summation notation, unlike Python's own `range`, which stops one short.

</details>

<details>
<summary>Hint 2</summary>

Handle the empty case (`hi < lo`) by starting `total = 0` and simply never entering the loop, rather than special-casing it separately — `range(lo, hi + 1)` is already empty in that case, so no extra branch is needed.

</details>

## Theory

### The simple version

`Σ_{i=1}^{5} i` reads as: "add up `i`, for every integer `i` from `1` to `5`." That's `1 + 2 + 3 + 4 + 5 = 15`. The letter under and over the `Σ` are just the loop's start and end; the expression to the right is the loop body.

### The formula

$$
\sum_{i=\text{lo}}^{\text{hi}} f(i) = f(\text{lo}) + f(\text{lo}+1) + \cdots + f(\text{hi})
$$

- `i` — the **index variable**, a name chosen by whoever writes the formula (often `i`, `j`, `k`, or a variable matching what's being summed over, like `x` for data points).
- `lo`, `hi` — the range's bounds, written below and above `Σ`, both **inclusive**.
- `f(i)` — the **summand**: whatever expression appears to the right of `Σ`, evaluated once per index and added to the running total.

### Where this shows up

Once you can read `Σ` as "loop and accumulate," every formula that uses it becomes readable as code before you even reach its Theory page:

- Mean: `(1/n) Σ_{i=1}^{n} x_i` — sum every data point, then divide by the count.
- Dot product: `Σ_{i=1}^{n} a_i b_i` — sum the products of corresponding entries.
- Cross-entropy: `-Σ_x p(x) log q(x)` — sum, over every outcome `x`, a per-outcome penalty term.

In every case, the summand (what's to the right of `Σ`) is the only thing that changes; the "loop and accumulate" structure is always identical.

### How code actually implements this

NumPy and PyTorch never write this loop explicitly for numeric data — `arr.sum()` and `tensor.sum()` compute the same accumulation in a single vectorized call, which is dramatically faster than a Python-level loop for large arrays (the exact reason is covered fully in the NumPy track's vectorization module). Writing the loop out by hand here, once, is what makes it obvious that `.sum()` is not a different operation, just a faster implementation of the identical idea.

## Explanation

`summation` starts `total = 0` and loops `i` over `range(lo, hi + 1)` — the `+ 1` is what turns Python's exclusive-stop `range` into the inclusive-on-both-ends range summation notation actually uses. Each iteration adds `f(i)` to `total`. When `hi < lo`, `range(lo, hi + 1)` is already empty, so the loop body never runs and the function correctly returns `0`, matching the standard convention that an empty sum is `0` without needing a special-cased branch.
