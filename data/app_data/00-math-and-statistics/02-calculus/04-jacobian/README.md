---
name: math-jacobian
title: 'Jacobian: the matrix of all partial derivatives of a vector-valued function'
tags: [calculus]
difficulty: Advanced
---

## Statement

### The problem, from first principles

`02-partial-derivatives`'s gradient answers "how does one number (a loss) respond to changes in many inputs." But most operations in a real network don't collapse down to one number, `linear` alone maps `in_features` inputs to `out_features` outputs, every one of which can respond differently to a nudge in any given input. You need the gradient's generalization: not one row of sensitivities, but a whole grid of them, one row per output, one column per input.

That grid is the Jacobian, and it is the object every "vector-in, vector-out" operation's backward pass is secretly built on top of, even though, as you'll see in the Autograd track, real backward passes are clever enough to never form the whole matrix explicitly.

### From theory to code

Theory generalizes `02-partial-derivatives`'s single-output gradient to many outputs at once: row `i` is output `i`'s own gradient. Implement it by evaluating `f` once to learn the output size, then, for each input coordinate, applying the central difference to the ENTIRE output vector simultaneously, filling in one column of the result per input coordinate.

Implement `jacobian(f, x, eps=1e-5)` against that reasoning. The signature and docstring are already in the editor.

### Constraints

- `f` takes a length-`n` vector and returns a length-`m` vector, or a scalar (treated as `m = 1`).
- Use `np.atleast_1d` on `f`'s output so both cases are handled uniformly.
- Result shape is always `(m, n)`: `m` rows (one per output), `n` columns (one per input).

### Hints

Open one at a time. Each gives away a little more than the last.

<details>
<summary>Hint 1</summary>

Call `f(x)` once, before the main loop, purely to learn `m` via `len(np.atleast_1d(f(x)))`. You'll then call `f` again inside the loop for the actual finite differences.

</details>

<details>
<summary>Hint 2</summary>

The loop is over input coordinates `j`, not output coordinates. Each iteration fills one entire COLUMN of the result, `result[:, j]`, using the same central-difference formula applied to a vector-valued `f` instead of a scalar one.

</details>

## Theory

### The simple version

A thermostat with one dial and one sensor has a single sensitivity number: turn the dial, read the one temperature. Now imagine a dial that simultaneously controls temperature AND humidity, and there are two dials. You no longer have one sensitivity number, you have four: how each dial affects each of the two readings. Arrange those four numbers in a grid, one row per reading, one column per dial, and you have a Jacobian.

### The formula

`02-partial-derivatives`'s `gradient` handles a function with many inputs but one scalar output. The **Jacobian** generalizes that one step further, to a function with many inputs AND many outputs:

```text
f: R^n -> R^m

J[i, j] = df_i / dx_j
```

Row `i` of the Jacobian is output `i`'s own gradient with respect to every input, so the Jacobian is really just `m` stacked gradients, one per output. Column `j` answers "if I nudge only input `j`, how does every output move at once", the same question `02-partial-derivatives` asked, just now recorded for every output simultaneously instead of one.

This is the natural shape for `linear`, this curriculum's first question: `linear(x, weight)` maps an `in_features`-dimensional input to an `out_features`-dimensional output, and its Jacobian with respect to `x` is exactly `weight` itself (a linear map's Jacobian is the map's own matrix, everywhere). Every backward pass through a layer with multiple outputs is, underneath, a Jacobian-vector product, even though this curriculum's autograd questions never form the full Jacobian explicitly (it would be far too large for real networks), computing the full matrix here, for small functions, is what makes the underlying object concrete before treating it as an implementation detail later.

### How PyTorch actually implements this

Real PyTorch deliberately avoids ever materializing the full Jacobian during ordinary training: for a layer mapping millions of inputs to millions of outputs, the Jacobian itself would be a matrix of trillions of entries, far too large to store. Instead, `loss.backward()` computes **Jacobian-vector products** (`04-softmax`'s and `02-cross-entropy`'s backward passes are both, secretly, closed-form Jacobian-vector products, derived analytically rather than by forming a matrix), which only ever need a vector the size of the output, not the full matrix. When the actual Jacobian genuinely is needed, for sensitivity analysis, certain numerical-stability diagnostics, or double-checking a custom `torch.autograd.Function`, `torch.autograd.functional.jacobian` computes it directly, using the same reverse-mode machinery one row (or, with the `vectorize` option, one batched pass) at a time, rather than the brute-force finite-difference approach this question implements.

## Explanation

`jacobian` evaluates `f(x)` once to determine the output size `m` (via `np.atleast_1d`, so a scalar-returning `f` is handled the same as a vector-returning one), allocates an `(m, n)` result, and for each input coordinate `j`, applies the central difference formula (`01-derivatives-first-principles`) to the entire output vector at once, filling in column `j`. This is exactly `02-partial-derivatives`'s `gradient`, generalized from "one partial derivative per input" to "one partial derivative _vector_ per input".
