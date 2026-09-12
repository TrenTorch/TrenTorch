---
name: math-partial-derivatives
title: Partial derivatives of a multivariate function
tags: [calculus]
difficulty: Beginner
---

## Statement

### The problem, from first principles

A single-variable derivative answers "how does output change as this one input changes." But a real loss function depends on hundreds, thousands, or millions of numbers at once, every weight and bias in a network. You can't ask "how does the loss change" without saying _which_ number you're wiggling, so the natural move is to ask the single-variable question over and over, once per number, holding everything else perfectly still each time.

That's a partial derivative. And collecting every one of those answers into a single vector, one entry per parameter, gives you the gradient, the object every optimizer in this curriculum (`04-gd-step` onward) actually steps against.

### From theory to code

Theory reduces a partial derivative to `01-derivatives-first-principles`'s central difference, applied to just one coordinate of a multi-dimensional input while every other coordinate stays fixed. Implement that first, then collect it across every coordinate to build the full gradient.

Implement `partial_derivative(f, x, index, eps=1e-5)` and `gradient(f, x, eps=1e-5)` against that reasoning. The signatures and docstrings are already in the editor.

### Constraints

- `f` takes a NumPy array `x` and returns a scalar.
- `partial_derivative` must not mutate the caller's `x`, copy before nudging.
- `gradient`'s output has the same shape as `x`, one partial derivative per coordinate, in the same order.

### Hints

Open one at a time. Each gives away a little more than the last.

<details>
<summary>Hint 1</summary>

`x.copy()` before nudging a single coordinate. Mutating the array a caller handed you is a silent bug waiting to happen.

</details>

<details>
<summary>Hint 2</summary>

`gradient` is a one-line loop (or list comprehension) calling `partial_derivative` once per index, it does no numerical work of its own.

</details>

## Theory

### The simple version

A chef adjusting a recipe with ten ingredients doesn't wonder "how does the dish change" in the abstract, they ask "what happens if I add a little more salt, everything else exactly the same," then separately ask the same question about the pepper, and the garlic, one ingredient at a time. Each of those isolated questions is a partial derivative. Write down the answer for every ingredient at once, in order, and you have the gradient: a complete list of "nudge this one thing, here's the effect," for every knob you could turn.

### The formula

Every loss function in this curriculum, `01-mse`, `02-cross-entropy`, `linear_regression`'s own MSE, depends on many numbers at once (every weight, every bias). A **partial derivative** asks: "if I nudge just one of those numbers, holding every other one fixed, how does the output change?"

```text
df/dx_i = (rate of change of f, moving only along coordinate i)
```

It is exactly `01-derivatives-first-principles`'s central difference, applied along a single axis of a multi-dimensional input instead of a single scalar `x`.

The **gradient** collects every partial derivative into one vector:

```text
gradient(f, x) = [df/dx_0, df/dx_1, ..., df/dx_n]
```

This is the object every training loop in this curriculum computes (via analytical backward passes, not finite differences, for speed) and uses to update parameters: `04-gd-step`'s gradient descent update, `weight - lr * grad_weight`, is stepping in the direction the gradient says decreases the loss fastest, a later question in this track makes that "steepest ascent/descent" interpretation explicit.

### How PyTorch actually implements this

Real PyTorch never computes a gradient by looping over parameters and finite-differencing each one, that would need two full forward passes per parameter, computationally hopeless for a network with millions of weights. Instead, `loss.backward()` computes every partial derivative simultaneously in a single backward traversal of the computation graph (reverse-mode automatic differentiation, the mechanism the Autograd track builds from scratch), and stores the result for each `nn.Parameter` in that tensor's own `.grad` attribute. Finite differences, exactly like the ones implemented here, exist in real PyTorch purely as a correctness check on that machinery (`torch.autograd.gradcheck`), never as the actual gradient-computation strategy in a training loop.

## Explanation

`partial_derivative` copies `x` twice, nudges only `x[index]` up in one copy and down in the other by `eps`, and applies the central difference formula to those two function evaluations, exactly `01-derivatives-first-principles`'s formula restricted to one coordinate.

`gradient` calls `partial_derivative` once per coordinate of `x` and collects the results into an array, the direct definition.
