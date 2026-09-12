---
name: dl-core-numerical-gradient-checking
title: 'Numerical gradient checking: verify an analytical gradient via finite differences'
tags: [neural-networks, autograd]
difficulty: Intermediate
---

## Statement

### The problem, from first principles

Every backward formula this entire curriculum has written, `03-tanh`'s `1 - output**2`, `03-mse-gradient`'s `grad_prediction.T @ input`, `Assemble minimal autograd engine`'s whole reverse-topological walk, is a place a mistake could have silently crept in: a dropped transpose, a sign flip, a wrong axis, a formula copied from the wrong nearby function. A backward formula with a subtle bug doesn't crash, it just quietly computes a WRONG gradient, that a model then trains against, producing a model that trains slower, or worse, or not at all, with no error message pointing at the actual cause.

Numerical gradient checking is the tool that catches this class of bug directly: compute the SAME gradient two completely independent ways, once analytically (the formula you wrote, that you're not fully sure is correct) and once numerically (`01-derivatives-first-principles`'s central difference, slow, but essentially impossible to get subtly wrong), and confirm they agree. This is, formalized into reusable code, the exact discipline this entire curriculum's authoring process has quietly relied on: every single backward formula built throughout this whole session was checked against something equivalent to this before being trusted.

### From theory to code

Theory computes the numerical gradient via central difference, compares it to a provided analytical gradient using a SCALE-INVARIANT relative error (rather than a raw absolute difference, which would be meaningless without knowing the gradient's typical magnitude), and returns whether that error falls below a tolerance.

Implement `numerical_gradient(f, x, eps=1e-5)` first, then `relative_error(analytical, numerical)`, then `gradient_check(f, x, analytical_grad, eps=1e-5, tolerance=1e-5)`.

### Constraints

- `numerical_gradient` is `01-derivatives-first-principles`'s exact central difference formula, restated here for a self-contained, standalone autograd utility.
- `relative_error` must handle the edge case where both gradients are (near) zero, without dividing by zero.
- `gradient_check` returns a plain `bool`.

### Hints

Open one at a time. Each gives away a little more than the last.

<details>
<summary>Hint 1</summary>

`(f(x + eps) - f(x - eps)) / (2 * eps)` is the entire `numerical_gradient` formula, no new derivation needed.

</details>

<details>
<summary>Hint 2</summary>

`max(abs(analytical), abs(numerical), 1e-12)` as the denominator keeps `relative_error` well-defined even when both gradients happen to be exactly `0`.

</details>

## Theory

### The simple version

A carpenter measures a board's length twice, once with a tape measure (quick, but relies on reading the marks correctly, a method that COULD have a mistake), once by comparing it against a board of already-known length (slower, more tedious, but essentially foolproof). If the two measurements disagree, trust the foolproof one, and go figure out what went wrong with the quick one. Gradient checking applies exactly this idea to a written backward formula: the analytical gradient is the quick, error-prone tape measure; the numerical gradient (central difference, `01-derivatives-first-principles`) is the slow, tedious, essentially-foolproof comparison method.

### The formula

```text
numerical_gradient(f, x) ~= (f(x + eps) - f(x - eps)) / (2 * eps)

relative_error(analytical, numerical) = |analytical - numerical| / max(|analytical|, |numerical|, 1e-12)

gradient_check(...) = relative_error(analytical_grad, numerical_gradient(f, x)) < tolerance
```

Using a RELATIVE error instead of a raw absolute difference matters: an absolute gap of `0.01` is a glaring, obvious bug when both gradients are around `0.001`, but is completely unremarkable rounding noise when both gradients are around `10000`. Dividing by the larger magnitude (floored at a tiny constant to stay defined when both gradients are legitimately near zero) makes the comparison meaningful regardless of the gradient's overall scale, exactly the same "compare on a normalized footing, not raw magnitude" idea `04-feature-scaling`'s standardization and `01-outlier-detection`'s z-score both use elsewhere in this curriculum.

A passing `gradient_check` (small relative error) is strong evidence the analytical formula is correct, but a FAILING check is even more valuable: it's a precise, actionable signal that something in that specific backward formula is wrong, exactly the kind of bug this curriculum's own "deliberately mutate the solution, confirm the tests catch it" authoring discipline exists to surface before ever shipping a formula that's silently incorrect.

### How PyTorch actually implements this

`torch.autograd.gradcheck` is this exact utility, generalized to vector- and tensor-valued functions, and it's run routinely inside PyTorch's own test suite: every time a new differentiable operation is added to the library, its hand-written (or auto-generated) backward formula gets checked against a numerical approximation like this one before it's trusted enough to ship. Any time you write a custom `torch.autograd.Function` with your own hand-derived `backward` method (a genuinely common need when implementing a novel operation PyTorch doesn't provide natively), `gradcheck` is the standard, expected way to verify it before trusting a single gradient it produces, precisely the discipline this question, and this entire curriculum's authoring process, is built around.

## Explanation

`numerical_gradient` evaluates `f` at `x + eps` and `x - eps` and applies the central difference formula directly.

`relative_error` computes `abs(analytical - numerical)` divided by whichever is larger between `abs(analytical)`, `abs(numerical)`, and a small floor constant `1e-12` (avoiding division by zero when both gradients are near zero).

`gradient_check` computes the numerical gradient, compares it to `analytical_grad` via `relative_error`, and returns whether that error falls below `tolerance`.
