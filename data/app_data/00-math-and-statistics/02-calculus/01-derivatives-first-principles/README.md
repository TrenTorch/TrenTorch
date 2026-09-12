---
name: math-derivatives-first-principles
title: 'Derivatives from first principles: the limit definition, computed numerically'
tags: [calculus]
difficulty: Beginner
---

## Statement

### The problem, from first principles

You're driving and want to know your speed at this exact instant, not your average speed over the whole trip. Speed is "distance per unit time", so a natural first attempt: look at the distance covered over a very short time window, and divide. Make that window shorter and shorter, and the answer stabilizes on your true instantaneous speed. That stabilizing process, "measure over an ever-shrinking window", is precisely what a derivative is, and precisely what a computer can approximate without ever taking an actual limit.

This isn't just a warm-up exercise: it's the tool every "did I compute this gradient correctly" check in this curriculum relies on. Every backward pass written from here on (`03-tanh`'s, `linear_regression`'s gradient, the entire Autograd track) can be sanity-checked by comparing its analytical answer against exactly the numerical approximation you build here.

### From theory to code

Theory gives two ways to approximate the limit with a small, finite step: one stepping only forward from `x`, one stepping symmetrically in both directions. Implement both, directly translating their formulas.

Implement `forward_difference(f, x, eps=1e-5)` and `central_difference(f, x, eps=1e-5)` against that reasoning. The signatures and docstrings are already in the editor.

### Constraints

- `f` is a plain Python function taking and returning a single number.
- `eps` defaults to `1e-5`, don't hardcode a different value.
- No symbolic differentiation, no calling a derivative library, only function evaluations of `f`.

### Hints

Open one at a time. Each gives away a little more than the last.

<details>
<summary>Hint 1</summary>

Both functions only ever call `f` at most twice. If you're calling it more than that, you've overcomplicated it.

</details>

<details>
<summary>Hint 2</summary>

`central_difference` steps by `eps` in both directions and averages the "rise" over `2 * eps`, not `eps`, since the total distance covered is twice the single step.

</details>

## Theory

### The simple version

Imagine reading your car's speedometer isn't possible, but you can read the odometer at any instant. To estimate your speed right now, note the odometer reading, wait a tiny fraction of a second, note it again, and divide the distance traveled by the time elapsed. The shorter that fraction of a second, the closer your estimate gets to your true instantaneous speed. A derivative is exactly this idea, made precise: the limit of that ratio as the time window shrinks to zero.

### The formula

The derivative of `f` at a point `x` is defined as a limit:

```text
f'(x) = lim (eps -> 0) [ (f(x + eps) - f(x)) / eps ]
```

"How much does `f` change, per unit of `x`, for an infinitesimally small step." A computer can't take an actual limit, but it can approximate one by using a small, finite `eps` instead of an infinitesimal one, this is called a **finite difference**, and it's the technique the Autograd track's numerical gradient checking uses to sanity-check every analytical backward pass this entire curriculum writes.

The **forward difference** is the direct translation of the limit definition, stepping only forward from `x`:

```text
f'(x) ~= (f(x + eps) - f(x)) / eps
```

The **central difference** instead steps symmetrically, forward and backward:

```text
f'(x) ~= (f(x + eps) - f(x - eps)) / (2 * eps)
```

Central difference is meaningfully more accurate for the same `eps`: a Taylor expansion shows forward difference's error shrinks linearly with `eps` (halving `eps` roughly halves the error), while central difference's error shrinks quadratically (halving `eps` cuts the error by roughly 4x). This is why every gradient-checking routine in practice uses the central form, not the forward one, it gets much closer to the true derivative for the same computational cost (one extra function evaluation).

### How PyTorch actually implements this

`torch.autograd.gradcheck`, the real utility PyTorch ships for exactly this "did I implement backward correctly" question, uses central difference internally by default, for exactly the accuracy reason Theory gives. It's run routinely inside PyTorch's own test suite whenever a new differentiable operation is added to the library: every custom `torch.autograd.Function`'s hand-written backward gets checked against a numerical approximation like this one before it's trusted, the same discipline this curriculum's own mutation-testing process applies to every solution.py.

## Explanation

`forward_difference` and `central_difference` both implement their respective formula from Theory directly, evaluating `f` at the shifted point(s) and dividing by the appropriate step size.
