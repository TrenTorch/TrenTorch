---
name: dl-core-sigmoid
title: Sigmoid fwd/bwd
tags: [deep-learning, activations, autograd]
difficulty: Beginner
---

## Statement

### The problem, from first principles

`01-relu`'s backward pass needed the _original input_ `x` to know which elements were positive. Sigmoid's backward pass has a different, more efficient option: its derivative can be written entirely in terms of its own _output_, so a real autograd engine never needs to keep the original input around at all once the forward pass has run.

### From theory to code

`01-classical-ml/02-classification`'s `sigmoid` already computed the forward formula, `1 / (1 + exp(-x))`. This question keeps that forward pass and adds `sigmoid_backward(grad_output, output)`, which takes the _saved forward output_, not `x`, a genuinely different signature from `01-relu`'s backward pass.

### Constraints

- `x`: any NumPy array shape. `sigmoid_forward` returns the same shape, values strictly in `(0, 1)`.
- `sigmoid_backward(grad_output, output)` takes the forward pass's own saved result, not the original `x`.
- `sigmoid_forward` must stay finite for any input, including very large `|x|`.
- No Python loops; no mutating the inputs.

### Hints

Open one at a time. Each gives away a little more than the last.

<details>
<summary>Hint 1</summary>

Sigmoid's derivative has a closed form written purely in terms of `sigmoid(x)` itself — you don't need `x` at all in `sigmoid_backward`.

</details>

<details>
<summary>Hint 2</summary>

`f'(x) = f(x) * (1 - f(x))` — multiply that factor into `grad_output`.

</details>

## Theory

### The simple version

Sigmoid's derivative peaks exactly where the function is most uncertain (output near `0.5`, the steepest part of the S-curve) and flattens out toward either extreme (output near `0` or `1`, where the curve is nearly level) — and remarkably, that entire shape can be read off from the output value alone, with no need to remember what raw input produced it.

### The formula

```text
forward:  y = sigmoid(x)
backward: dL/dx = dL/dy * y * (1 - y)     -- needs y (the SAVED output), not x
```

This matters in practice: a real autograd engine (like the one `04-autograd`'s progressive build assembles later in this section) has to decide what to _save_ from the forward pass for the backward pass to use later. Saving `y` instead of `x` for a sigmoid, whenever both would work, is a real memory-efficiency choice, and for sigmoid specifically, `y` is strictly sufficient — there's never a reason to also keep `x` around.

### How PyTorch actually implements this

Context only, untested by your submission: `torch.sigmoid` (and `nn.Sigmoid`) compute the same forward formula, and PyTorch's autograd saves exactly the forward output (not the input) to compute this backward pass efficiently — the same `y * (1 - y)` factor this exercise implements by hand.

## Explanation

`sigmoid_forward` clips `x` to `[-500, 500]` before exponentiating (the same guard `01-classical-ml`'s own `sigmoid` uses) — `exp` of a very large negative number underflows harmlessly to `0`, but `exp` of a very large _positive_ number (from `-x` when `x` is very negative) can overflow to `inf`; clipping the input keeps the exponent itself bounded.

`sigmoid_backward` is the formula directly, `grad_output * output * (1 - output)` — the chain rule applied using only the saved forward output, exactly as Theory describes, with no recomputation of `sigmoid_forward` and no need for the original `x` anywhere in this function.
