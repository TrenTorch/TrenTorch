---
name: math-directional-derivatives
title: 'Directional derivatives, and the gradient as steepest ascent'
tags: [calculus, optimization]
difficulty: Intermediate
---

## Statement

### The problem, from first principles

Standing on a hillside, "how steep is it here" isn't a complete question, steepness depends entirely on which way you're facing. Walk along a contour line and it's flat; walk straight up the slope and it's as steep as it gets. `02-partial-derivatives` only ever asked about steepness along the coordinate axes (due east, due north). This question asks the more general version: how steep is it in ANY direction you choose, and, crucially, which single direction is steepest of all.

That "which direction is steepest" answer turns out to be the gradient itself, not just a bookkeeping vector of per-axis sensitivities but a genuine compass pointing the way uphill fastest. This is the fact that makes gradient descent (`04-gd-step`) actually work: stepping opposite the gradient isn't an arbitrary heuristic, it's stepping in the single most effective downhill direction available.

### From theory to code

Theory shows a directional derivative is just `01-derivatives-first-principles`'s central difference, evaluated by stepping along an arbitrary unit vector instead of a coordinate axis, and that the gradient, normalized to unit length, IS the direction of steepest increase. Implement both directly, reusing `02-partial-derivatives`'s `gradient` for the second one.

Implement `directional_derivative(f, x, direction, eps=1e-5)` and `steepest_ascent_direction(f, x)` against that reasoning. The signatures and docstrings are already in the editor.

### Constraints

- `direction` is not guaranteed to already be a unit vector, normalize it first.
- `steepest_ascent_direction` returns a unit vector (norm 1), pointing in the gradient's direction, not the raw gradient itself.

### Hints

Open one at a time. Each gives away a little more than the last.

<details>
<summary>Hint 1</summary>

`direction / np.linalg.norm(direction)` turns any nonzero vector into a unit vector pointing the same way.

</details>

<details>
<summary>Hint 2</summary>

`steepest_ascent_direction` needs no new numerical machinery: compute the gradient, then normalize it the same way you normalized `direction` above.

</details>

## Theory

### The simple version

Standing on a hillside, ask "how steep is it" and the honest answer is "which way are you facing?" Walk along the side of the hill (a contour line) and it feels flat. Walk straight up and it's as steep as the hill gets. A directional derivative is exactly this: how fast the ground rises, measured along whichever direction you pick.

### The formula

The directional derivative of `f` at `x`, along a unit vector `u`, generalizes `01-derivatives-first-principles`'s central difference from stepping along one axis to stepping along any direction at all:

```text
D_u f(x) ~= (f(x + eps*u) - f(x - eps*u)) / (2 * eps)
```

`02-partial-derivatives`'s partial derivatives are the special case where `u` is a coordinate axis (`[1, 0, ...]`, `[0, 1, ...]`, etc.).

The remarkable fact, proven via the gradient's own definition: the directional derivative along unit vector `u` equals `gradient(f, x) . u` (a plain dot product). Since a dot product between two vectors is maximized when they point the same way, the direction that maximizes the directional derivative, the direction of steepest ascent, is exactly the gradient itself, normalized to a unit vector:

```text
steepest_ascent_direction(f, x) = gradient(f, x) / ||gradient(f, x)||
```

This is the mathematical justification for gradient descent (`04-gd-step`): `weight - lr * grad_weight` steps opposite the gradient specifically because the gradient is the direction of steepest increase, so its negative is the direction of steepest decrease, the most effective single direction to reduce a loss.

### How PyTorch actually implements this

Every optimizer in `torch.optim` (SGD, Adam, and the rest, covered in the Optimizers track) is built on exactly this fact: `parameter.grad`, populated by `loss.backward()`, IS the direction of steepest ascent at the current parameters, and every update rule subtracts some function of it. Momentum-based optimizers refine this by not stepping purely along the instantaneous steepest-ascent direction (which can zigzag on a curved loss surface) but along a running average of recent gradients, still fundamentally built on the same "gradient points uphill, step the other way" fact this question derives directly.

## Explanation

`directional_derivative` normalizes `direction` to a unit vector, then applies `01-derivatives-first-principles`'s central difference formula with that unit vector standing in for `eps`'s single-axis step, evaluating `f` at `x` shifted forward and backward along the whole direction at once.

`steepest_ascent_direction` computes the full gradient via the provided `gradient` function and divides by its own norm, turning it into a unit vector pointing the same way, per Theory's steepest-ascent formula.
