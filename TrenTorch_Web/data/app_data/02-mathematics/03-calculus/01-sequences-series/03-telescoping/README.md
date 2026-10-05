---
name: math-telescoping-series
title: Telescoping Series
tags: [calculus, series]
difficulty: Intermediate
---

## Statement

### The problem, from first principles

`01-geometric` found a closed form by multiplying a sum by `r` and subtracting so that almost every term cancelled. Some series cancel without any trick at all: each term contains a piece that the next term subtracts away, like the sections of a collapsing spyglass sliding into each other until only the two ends remain. Spotting that structure turns a sum of a million terms into a single subtraction. This question implements it, and applies it to a series that does not look like it cancels until it is rewritten.

### From theory to code

Implement `telescoping_partial_sum(f, n)`, the sum of the first `n` terms of the series with terms `f(k) - f(k + 1)`, then `telescoping_infinite_sum(f_first, f_limit)`, the sum of the infinite series, then `sum_reciprocal_products(n)`, the sum of `1 / (k * (k + 1))` for `k` from 1 to `n`. The signatures and docstrings are already in the editor.

### Constraints

- `f` is a function taking an integer and returning a float. The series is `(f(1) - f(2)) + (f(2) - f(3)) + ...`.
- `telescoping_partial_sum` takes an integer `n >= 0`, calls `f` exactly twice for any `n >= 1`, and never loops over the terms. With `n = 0` it returns `0.0` and does not call `f`.
- `telescoping_infinite_sum` receives the value `f(1)` and the limit of `f(k)` as `k` grows. It does not need `f` itself.
- `sum_reciprocal_products` takes an integer `n >= 0` and returns a float. It must not loop over the terms and must return exactly `0.0` for `n = 0`.

### Hints

<details>
<summary>Hint 1</summary>

Write out the first four terms of `(f(1) - f(2)) + (f(2) - f(3)) + ...` and cross out whatever appears once with each sign. Only two values survive, however many terms there are.

</details>

<details>
<summary>Hint 2</summary>

`1 / (k * (k + 1))` is not written as a difference of consecutive values yet, but it splits into two simple fractions with denominators `k` and `k + 1`. Find the two numerators, and the series becomes `f(k) - f(k + 1)` for a very simple `f`.

</details>

## Theory

### The simple version

Picture a row of dominoes where each one, as it falls, knocks the next one back up. After a thousand dominoes, nothing is left standing except what happened at the very start and at the very end. A telescoping series works the same way: every term hands something to the next term and takes it back, so all the middle cancels and only the ends remain.

### The formula

For terms of the form $f(k) - f(k+1)$,

$$
\sum_{k=1}^{n} \big(f(k) - f(k+1)\big) = f(1) - f(n+1)
$$

because $-f(2)$ cancels $+f(2)$ from the next term, $-f(3)$ cancels $+f(3)$, and so on until only $f(1)$ at the front and $-f(n+1)$ at the back are left. The infinite series is the limit of this as $n$ grows. If $f(k) \to L$, then

$$
\sum_{k=1}^{\infty} \big(f(k) - f(k+1)\big) = f(1) - L
$$

If $f(k)$ has no limit, the series has no sum.

### Making a series telescope

Most telescoping series arrive disguised. The usual disguise is a fraction that splits into a difference by **partial fractions**:

$$
\frac{1}{k(k+1)} = \frac{1}{k} - \frac{1}{k+1}
$$

so with $f(k) = 1/k$ the sum is

$$
\sum_{k=1}^{n} \frac{1}{k(k+1)} = 1 - \frac{1}{n+1} = \frac{n}{n+1}
$$

which tends to 1. Without the rewrite, the terms $1/2, 1/6, 1/12, \dots$ give no hint of that answer.

### Where this shows up in machine learning

Convergence proofs for gradient descent lean on exactly this. If $L_t$ is the loss at step $t$ and each step lowers it, then the total improvement $\sum_{t=0}^{T-1}(L_t - L_{t+1})$ telescopes to $L_0 - L_T$. Since $L_T$ cannot go below the minimum loss, the total improvement is bounded, which forces the per-step improvements to shrink. The same collapse underlies the derivation of the log-likelihood chain rule and several variance-reduction identities.

### How NumPy/PyTorch actually implements this

There is nothing to implement: the point of the technique is that no library call is needed. Checking the algebra numerically is a one-liner, though, `np.cumsum` of the terms compared against the closed form, and `np.diff` is the discrete operation that telescoping sums undo (summing differences gives back the endpoint difference).

## Explanation

`telescoping_partial_sum` returns `f(1) - f(n + 1)`, two evaluations regardless of `n`, and returns `0.0` for `n = 0` before touching `f`, since an empty sum has no terms to cancel. `telescoping_infinite_sum` is the limit form: the back end `f(n + 1)` has been replaced by its limit, so the answer is `f_first - f_limit`. `sum_reciprocal_products` uses the partial-fraction split `1/k - 1/(k + 1)` to see that the series telescopes with `f(k) = 1/k`, which gives `1 - 1/(n + 1)`; it is written as `n / (n + 1)` because that form returns exactly `0.0` at `n = 0` with no subtraction of nearly equal numbers.
