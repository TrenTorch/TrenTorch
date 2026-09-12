---
name: math-hessian
title: 'Hessian: second-order partial derivatives, and what its eigenvalues tell you'
tags: [calculus, optimization]
difficulty: Advanced
---

## Statement

### The problem, from first principles

A gradient of zero tells you a function is momentarily flat, but flat could mean you're at the bottom of a bowl (great, you're done), the top of a hill (terrible, you want to be anywhere else), or on a mountain pass that's flat in one direction and steeply curved in another (a saddle, training can get stuck circling one of these). The gradient alone genuinely cannot distinguish these three situations, it only knows "flat right here," not "which way does flat curve."

The Hessian is the tool that answers "which way does it curve": the full matrix of second derivatives, one entry for every pair of input coordinates. And, as `08-positive-definite-matrices` already set up, its eigenvalues turn that matrix into a clean, three-way answer.

### From theory to code

Theory frames the Hessian as literally the Jacobian of the gradient, which means you already have every piece needed to build it: `04-jacobian`'s central-difference-over-a-vector-valued-function structure, applied to `gradient` (from `02-partial-derivatives`) instead of to `f` directly. Implement that, then use `08-positive-definite-matrices`'s eigenvalue-sign logic to classify a critical point.

Implement `hessian(f, x, eps=1e-4)` and `classify_critical_point(hessian_matrix)` against that reasoning. The signatures and docstrings are already in the editor.

### Constraints

- `f` is scalar-valued (`R^n -> R`), `hessian`'s result is always `(n, n)`.
- Use the provided `gradient` (imported at the top of the file) as the thing you're differentiating, don't call `f` directly inside `hessian`.
- `classify_critical_point` must use a small tolerance around zero when checking eigenvalue signs, not a bare `> 0`/`< 0`.

### Hints

Open one at a time. Each gives away a little more than the last.

<details>
<summary>Hint 1</summary>

The Hessian is the Jacobian of the gradient. If you already understand `04-jacobian`, you already understand the loop structure this question needs, just swap which function is being differentiated.

</details>

<details>
<summary>Hint 2</summary>

`np.linalg.eigvalsh` (from `06-eigenvalues-eigenvectors`/`08-positive-definite-matrices`) gives you the eigenvalues directly. Check whether every one is comfortably positive, comfortably negative, or neither.

</details>

## Theory

### The simple version

Imagine feeling the ground with your feet at a spot where it's perfectly level. Level alone doesn't tell you if you're at the bottom of a valley, the top of a hill, or on a ridge that's level only in one exact direction. To know which, you'd need to feel how the ground curves as you take a small step in every direction. The Hessian is exactly that: it records how the _slope itself_ is changing, in every direction, at that one point.

### The formula

The Hessian of a scalar function `f: R^n -> R` is the matrix of all its second partial derivatives:

```text
H[i, j] = d^2f / (dx_i dx_j)
```

Equivalently, and this is the key insight for implementing it: **the Hessian is the Jacobian of the gradient**. The gradient (`02-partial-derivatives`) is itself a vector-valued function of `x` (it has one output per input coordinate), so applying `04-jacobian`'s exact machinery to `gradient` instead of to `f` directly produces the Hessian for free.

At a critical point (where the gradient is zero), the Hessian's eigenvalues (`06-eigenvalues-eigenvectors`, `08-positive-definite-matrices`) classify what kind of point it is:

```text
every eigenvalue > 0  -> local minimum   (the Hessian is positive-definite: curves up everywhere)
every eigenvalue < 0  -> local maximum   (curves down everywhere)
mixed signs            -> saddle point    (curves up some ways, down others)
```

This is the exact test that certifies a training loop has actually found a good minimum, rather than merely a flat spot: `08-positive-definite-matrices`'s "why it matters for optimization" section names this precise use case.

### How PyTorch actually implements this

Full Hessians are almost never computed during ordinary neural network training, for an `n`-parameter model the Hessian is `(n, n)`, and `n` is routinely in the millions or billions, far too large to store or invert. Where Hessian information genuinely matters, second-order optimizers like L-BFGS (`torch.optim.LBFGS`), or Hessian-vector products used in some meta-learning and curvature-aware training methods, PyTorch computes `torch.autograd.functional.hessian` (or, more commonly, just a Hessian-_vector_ product via two nested `autograd.grad` calls) using exact reverse-mode automatic differentiation twice in a row, never finite differences, since finite-differencing a finite-differenced gradient (as this question does, for teaching purposes) compounds numerical error badly at scale.

## Explanation

`hessian` loops over each input coordinate `i`, nudges it up and down by `eps`, evaluates the full `gradient` (not `f` itself) at each nudged point, and central-differences those two gradient vectors to fill column `i` of the result, exactly `04-jacobian`'s structure with `gradient` standing in for `f`. A larger `eps` than `01-derivatives-first-principles`'s default is used because differentiating an already-approximate `gradient` amplifies floating-point error.

`classify_critical_point` computes the Hessian's eigenvalues via `np.linalg.eigvalsh` and checks their signs against a small tolerance (`1e-6`) rather than exactly `0`, returning `"minimum"`, `"maximum"`, or `"saddle"` per Theory's three-way rule.
