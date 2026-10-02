---
name: math-combinatorics
title: 'Combinatorics: Permutations and Combinations'
tags: [probability, foundations]
difficulty: Beginner
---

## Statement

### The problem, from first principles

`02-pmf-and-pdf`'s Binomial PMF leaned on `binom{n}{k}`, "n choose k," without deriving it — this question fills that gap by building the two counting tools every discrete-probability formula eventually needs: **permutations** (how many ways to arrange `k` items out of `n`, where order matters — who finishes 1st/2nd/3rd in a race) and **combinations** (how many ways to _choose_ `k` items out of `n`, where order doesn't matter — who's on a 3-person committee). Every discrete distribution built from "count the favorable outcomes, divide by total outcomes" — Binomial, Hypergeometric, Multinomial — starts here.

### From theory to code

Implement `permutations_count(n, k)` and `combinations_count(n, k)`, using Python's `math.factorial`. The signatures and docstrings are already in the editor.

### Constraints

- `n` and `k` are non-negative integers with `0 <= k <= n`.
- Use `math.factorial`, already imported in the starter.

### Hints

<details>
<summary>Hint 1</summary>

`permutations_count(n, k)` is `n! / (n-k)!` directly — Python's `//` performs exact integer division here since the result is always a whole number.

</details>

<details>
<summary>Hint 2</summary>

`combinations_count(n, k)` is `permutations_count(n, k)` divided again by `k!` — order-matters count, divided by the number of orderings of the `k` chosen items, removes the "order" information and leaves just "which items."

</details>

## Theory

### The simple version

Picture choosing a 3-person relay team from 5 runners, then deciding who runs which leg. "Which 3 runners are on the team" is a **combination** — `{Alice, Bob, Carol}` is the same team regardless of the order you name them. "Which runner goes 1st/2nd/3rd" is a **permutation** — `Alice-Bob-Carol` and `Carol-Bob-Alice` are different race plans even though they use the same 3 people. Combinations are always permutations "with the ordering thrown away," which is exactly what dividing by `k!` in the formula below does.

### The formula

$$
P(n, k) = \frac{n!}{(n-k)!} \qquad C(n, k) = \binom{n}{k} = \frac{n!}{k!(n-k)!}
$$

- `n!` — "n factorial," the number of ways to arrange all `n` items in a line (see `00-notation-and-foundations/03-factorial-and-binomial-coefficient`).
- `P(n, k)` — permutations of `n` items taken `k` at a time; order matters.
- `binom{n}{k}` / `C(n, k)` — combinations, "n choose k"; order doesn't matter. Read aloud as "n choose k."

### Where the k! in the denominator comes from

`P(n, k)` counts every ordered arrangement of `k` chosen items. Each _unordered_ group of `k` items corresponds to exactly `k!` different ordered arrangements (every way of reordering those same `k` items). So `C(n, k) = P(n, k) / k!` — dividing out the `k!` orderings that all correspond to "the same group" is precisely what turns an ordered count into an unordered one.

### How NumPy/PyTorch actually implements this

Python's own `math.perm(n, k)` and `math.comb(n, k)` (used directly in `02-pmf-and-pdf`'s `binomial_pmf`) compute exactly these two quantities, using an internal algorithm that avoids computing the full factorials separately (which would overflow for large `n` faster than necessary) — this question builds them from `math.factorial` directly to make the derivation explicit before relying on the built-in shortcut.

## Explanation

`permutations_count` computes `math.factorial(n) // math.factorial(n - k)` — the direct translation of `n!/(n-k)!`, using integer floor division (`//`) since the mathematical result is always an exact integer. `combinations_count` divides that same permutation count one step further by `math.factorial(k)`, implementing `n!/(k!(n-k)!)` and matching the "orderings removed" derivation above.
