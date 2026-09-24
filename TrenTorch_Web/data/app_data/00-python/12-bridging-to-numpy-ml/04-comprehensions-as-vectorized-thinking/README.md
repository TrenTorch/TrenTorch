---
name: python-numpy-bridge-comprehensions-as-vectorized-thinking
title: Comprehensions and Functional Thinking as Vectorized Thinking
tags: [python-numpy-bridge]
difficulty: Intermediate
---

## Statement

Implement small "whole-collection" operations (element-wise application, masking, broadcasting, and normalization) using comprehensions and `zip`, mirroring how vectorized array operations are expressed.

## Theory

Comprehensions, functions as values, and `map`/`filter` together express a way of thinking: describe **what the result is for the whole collection**, instead of writing the steps to fill it in position by position.

| Whole-collection idea | Comprehension form | Array-library form |
|---|---|---|
| Element-wise map | `[f(x) for x in xs]` | `f(arr)` |
| Combine positions | `[a + b for a, b in zip(xs, ys)]` | `xs + ys` |
| Mask selection | `[x for x, keep in zip(xs, mask) if keep]` | `arr[mask]` |
| Reduction | `sum(xs)`, `sum(xs) / len(xs)` | `arr.sum()`, `arr.mean()` |
| Broadcasting | `[x + 1 for x in xs]` | `arr + 1` |

**Broadcasting** treats a single number as if repeated to match the collection's length. The duck-typing test `hasattr(other, "__len__")` is a direct way to tell a scalar from a sequence.

**Normalization** rescales a vector to zero mean and unit variance:

$$\mu = \frac{1}{n}\sum x_i \qquad \sigma^2 = \frac{1}{n}\sum(x_i - \mu)^2 \qquad \hat{x}_i = \frac{x_i - \mu}{\sqrt{\sigma^2 + \epsilon}}$$

$\epsilon$ prevents division by zero when all values are equal. This is two reductions (mean, then mean of squared differences) plus one element-wise map broadcasting the two scalars $\mu$ and $\sigma^2 + \epsilon$ against every element.

**What a comprehension does not change.** It's still an interpreted loop — writing code in this style just makes the translation to array operations mechanical.

**Where this matters later.** Layer normalization's forward pass has exactly this shape: a mean, a variance, and a broadcasted element-wise expression.

## Explanation

`elementwise` uses `zip(*vectors)` — unpacking the variable number of input lists into `zip`'s own arguments — so it naturally stops at the shortest input and works for any number of vectors (including zero, where `zip()` with no arguments yields nothing and the comprehension produces `[]`). `broadcast_add` checks `hasattr(other, "__len__")` to decide scalar vs. sequence rather than `isinstance(other, list)`, which is exactly the duck-typing test from the previous topic and is what lets a tuple or another sequence type work as `other` too. `normalize` computes `mean` and `variance` as two separate reduction passes before the final comprehension, since the element-wise formula needs both finished scalars already in hand — it can't be done in a single pass over `values`.
