---
name: dl-core-relu
title: ReLU fwd/bwd
tags: [deep-learning, activations, autograd]
difficulty: Beginner
---

## Statement

### The problem, from first principles

Stacking linear layers on top of each other, with nothing in between, is still just one linear layer — matrix multiplications compose into another matrix multiplication, no matter how many you chain. A network needs a nonlinearity between its linear layers to represent anything more expressive than a straight line, and ReLU is the simplest one that still works well in practice: it passes positive signals through untouched and kills negative ones outright.

### From theory to code

Implement `relu_forward(x)`, the elementwise `max(0, x)`, and `relu_backward(grad_output, x)`, which needs to know which elements of the *original input* `x` were positive in order to decide how much of the incoming gradient to let through at each position.

### Constraints

- `x`, `grad_output`: any matching NumPy array shape.
- `relu_forward` returns the same shape as `x`, every entry either `0` or the original positive value.
- `relu_backward` takes the incoming `grad_output` and the original forward-pass input `x` (not the forward output), and returns a same-shape gradient.
- `relu_backward`'s gradient at exactly `x == 0` is `0` (PyTorch's own convention, one of several mathematically defensible choices at a non-differentiable point, but the one real PyTorch uses).
- No Python loops; no mutating `x` or `grad_output`.

### Hints

Open one at a time. Each gives away a little more than the last.

<details>
<summary>Hint 1</summary>

`relu_forward` is one NumPy call: an elementwise maximum against `0`.

</details>

<details>
<summary>Hint 2</summary>

`relu_backward` needs a `0`/`1` mask of "was this input positive," the same shape as `x` — build it with a comparison, then multiply it into `grad_output`.

</details>

## Theory

### The simple version

Think of ReLU as a one-way valve: positive signal flows through completely unchanged, negative signal is blocked entirely. During the backward pass, the valve remembers which way it was open — a gradient trying to flow back through a position that was blocked on the way forward gets blocked again, since nudging a zeroed-out input can't have changed the zeroed-out output.

### The formula

```text
forward:  y = max(0, x)
backward: dL/dx = dL/dy * (1 if x > 0 else 0)
```

The backward pass needs the *original input* `x` (not the forward output `y`), specifically to know which elements were positive — this is a genuinely different requirement from some of the later activation questions in this track, whose backward passes turn out to be cheaper to compute from their own *output* instead.

### How PyTorch actually implements this

Context only, untested by your submission: `torch.relu` (and `nn.ReLU`) compute exactly `max(0, x)` for the forward pass, and PyTorch's autograd derives the backward pass shown above automatically — the `0`-at-exactly-`0` convention this exercise specifies is the same one PyTorch's own implementation uses.

## Explanation

`relu_forward` is `np.maximum(0.0, x)` directly — the elementwise max operation is the entire definition, no further logic needed.

`relu_backward` builds a mask, `(x > 0).astype(grad_output.dtype)`, `1.0` wherever the original input was positive, `0.0` everywhere else (including exactly at `0`), and multiplies it into `grad_output` elementwise — this is the chain rule: the incoming gradient passes through unchanged wherever ReLU's slope was `1`, and gets zeroed out wherever ReLU's slope was `0`.
