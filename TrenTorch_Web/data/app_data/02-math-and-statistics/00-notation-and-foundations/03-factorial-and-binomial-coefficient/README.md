---
name: math-factorial-and-binomial-coefficient
title: 'Factorial and the Binomial Coefficient (n choose k)'
tags: [notation, foundations]
difficulty: Beginner
---

## Statement

### The problem, from first principles

"How many ways can you arrange `n` distinct items in a row?" and "how many ways can you pick `k` items out of `n`, where order doesn't matter?" are two of the most common counting questions in probability — and both have short, closed-form answers built directly out of `02-product-notation`'s `∏`. This question implements both, since the second (the binomial coefficient) is exactly what the Binomial distribution later in this track counts with.

### From theory to code

Implement `factorial(n)` first, then `n_choose_k(n, k)` in terms of it. The signatures and docstrings are already in the editor.

### Constraints

- `n` and `k` are non-negative integers, with `0 <= k <= n` for `n_choose_k`.
- `factorial(0) == 1` (the empty-product convention from `02-product-notation`).
- Return integers, not floats, even though the intermediate division in `n_choose_k` could otherwise produce one.

### Hints

<details>
<summary>Hint 1</summary>

`factorial(n)` is `∏_{i=1}^{n} i` — the exact same accumulate-by-multiplying loop as `02-product-notation`'s `product`, just written out directly here rather than imported (every question's `solution.py` is self-contained).

</details>

<details>
<summary>Hint 2</summary>

Use integer division (`//`) for the final division in `n_choose_k`, since the numerator is always exactly divisible by the denominator for valid `n`/`k` — the result is a count, and counts are integers.

</details>

## Theory

### The simple version

`5!` ("5 factorial") means "how many ways can you arrange 5 distinct objects in a row?" — pick any of the 5 for the first slot, any of the remaining 4 for the second, and so on: `5 × 4 × 3 × 2 × 1 = 120`. `n choose k`, written `C(n, k)` or `(n k)` (`n` over `k`, no division bar), answers a related but different question: "how many ways can you pick an **unordered** group of `k` items out of `n`?" — fewer ways than arranging, since picking `{a, b}` and `{b, a}` count as the same group.

### The formula

$$
n! = \prod_{i=1}^{n} i \qquad\qquad C(n, k) = \binom{n}{k} = \frac{n!}{k!(n-k)!}
$$

- `n!` — the factorial of `n`, the product of every integer from `1` to `n`.
- `C(n, k)` — the number of size-`k` subsets of an `n`-element set, read "n choose k".
- The `k!` in the denominator divides out the `k!` ways to _order_ a chosen group of `k` items (since order doesn't matter for a subset); the `(n-k)!` divides out the ways to order the items that were **not** chosen (since a subset is fully determined by only which items are in it, not by anything about the ones left out).

### Why the formula has that exact shape

`n!` counts every possible ordered arrangement of all `n` items. Every one of those `n!` arrangements can be split into three independent choices: which `k` items land in the "chosen" group (what we actually want to count), in what order those `k` chosen items happen to appear (`k!` possibilities, all counted as the same subset), and in what order the remaining `n-k` items happen to appear (`(n-k)!` possibilities, irrelevant to the subset itself). Dividing `n!` by both of those irrelevant orderings leaves exactly the count of distinct subsets.

### Where this shows up

The Binomial distribution (`03b-common-distributions`) uses `C(n, k)` directly: the probability of exactly `k` successes in `n` independent coin flips is `C(n, k) × p^k × (1-p)^(n-k)` — `C(n, k)` counts _how many_ of the `2^n` possible flip sequences have exactly `k` heads, since any specific sequence with `k` heads has the same probability `p^k (1-p)^(n-k)` regardless of which positions the heads land in.

### How code actually implements this

Python's standard library already has both: `math.factorial(n)` and `math.comb(n, k)`. Real code should use those directly rather than reimplementing them (they're implemented in C and handle large `n` without overflow); implementing them here once, by hand, from the `∏` they're built on, is what makes `math.comb`'s result legible as "a count of subsets" rather than an opaque library call.

## Explanation

`factorial(n)` accumulates `∏_{i=1}^{n} i` with the same loop shape as `02-product-notation`'s `product`, starting at `1` so `factorial(0)` correctly returns `1` with no special case. `n_choose_k(n, k)` computes `factorial(n) // (factorial(k) * factorial(n - k))`, using integer division since the binomial coefficient is always a whole number for valid inputs (every possible subset is counted exactly once, so the division has no remainder).
