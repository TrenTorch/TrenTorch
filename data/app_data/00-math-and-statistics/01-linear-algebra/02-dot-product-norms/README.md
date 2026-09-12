---
name: math-dot-product-norms
title: Dot product and vector norms (L1, L2, L-infinity)
tags: [linear-algebra, vectors]
difficulty: Beginner
---

## Statement

### The problem, from first principles

Say two friends rank the same five restaurants, one through five. How similar are their tastes? One way to answer: multiply their scores for each restaurant together and add the products up. If they agree (both love the same places, both hate the same places), the products are all large and positive; if they disagree, some products come out negative and cancel the rest. That single number, "multiply corresponding entries, then add," is the dot product, and it is doing real work here: it's a similarity score, computed without ever explicitly comparing "restaurant 1 vs restaurant 1."

Separately: how do you measure how "big" a vector is at all? "Big" turns out not to have one answer. A weight vector with one huge entry and the rest zero, and one with many small entries that sum to the same total, can be equally "big" by one measure and wildly different by another. Three specific ways of measuring size, L1, L2, L-infinity, show up constantly once you start regularizing models and clipping gradients, and this question is where you build the vocabulary for all three.

### From theory to code

Theory gives the exact formula for the dot product (sum of elementwise products) and for each norm. Implement all four as simple, direct translations of those formulas, no loops.

Implement `dot_product`, `l1_norm`, `l2_norm` and `linf_norm` against that reasoning. The signatures and docstrings are already in the editor.

### Constraints

- `a` and `b` (for `dot_product`) are 1D arrays of the same length.
- Every function returns a plain Python `float`, not a 0-d NumPy array.
- No explicit Python loop over vector entries anywhere.

### Hints

Open one at a time. Each gives away a little more than the last.

<details>
<summary>Hint 1</summary>

`dot_product` is exactly `elementwise_multiply` (an earlier question) followed by a sum over everything.

</details>

<details>
<summary>Hint 2</summary>

`l2_norm(x)` and `dot_product(x, x)` are related by a single square root, you don't have to derive it from scratch twice.

</details>

## Theory

### The simple version

Imagine two friends each ranking five restaurants from -2 (hate it) to +2 (love it). Multiply their scores for restaurant 1, then restaurant 2, and so on, then add every product together. If their tastes line up, the products are mostly positive and the total is large; if their tastes clash, some products go negative and cancel out the rest. That running total, "multiply matching entries, then add," is the **dot product**.

A **norm** answers a different question: not "how similar are two vectors" but "how big is one vector, as a single number."

### The formula

```text
a . b = sum_i(a_i * b_i)
```

Three norms are used constantly in ML, each with a different personality:

```text
L1 norm:   ||x||_1   = sum_i(|x_i|)          -- sum of magnitudes
L2 norm:   ||x||_2   = sqrt(sum_i(x_i^2))    -- straight-line ("Euclidean") length
Linf norm: ||x||_inf = max_i(|x_i|)          -- the single largest entry
```

The L2 norm is exactly `sqrt(x . x)` (the dot product of a vector with itself), which is why the dot product and norms belong in the same question. Each norm encodes a different notion of "big": L1 treats many small nonzero entries and one huge entry as comparably "big" if their totals match (this is what makes L1-regularization, seen in a later Stretch question, push weights to exactly zero rather than just small); L2 penalizes one huge entry far more than many small ones (a single outlier dominates a sum of squares); L-infinity cares about nothing but the worst single entry, ignoring everything else entirely.

### How PyTorch actually implements this

`torch.dot` and `torch.linalg.vector_norm` (the general form behind `torch.norm`) dispatch to BLAS routines under the hood (`sdot`/`ddot` for the dot product, a fused reduction kernel for norms) rather than a Python-level sum, the same reason a hand-written loop over a large vector is orders of magnitude slower in practice. Gradient clipping, seen later in the Optimizers track, calls `torch.nn.utils.clip_grad_norm_`, which computes exactly the L2 norm derived here across every parameter's gradient, then rescales if it exceeds a threshold, one of the most common places these three functions appear in a real training loop.

## Explanation

`dot_product` computes the elementwise product and sums it, `np.sum(a * b)`, the direct definition.

`l1_norm` sums `np.abs(x)`. `l2_norm` sums `x**2` and takes the square root, equivalent to `sqrt(dot_product(x, x))`. `linf_norm` takes `np.max(np.abs(x))`. All four return a plain Python `float`, not a 0-d array, matching what a scalar-valued function should hand back.
