---
name: seq-rnn-cell-backward
title: 'Vanilla RNN cell, backward'
tags: [nlp, neural-networks, autograd]
difficulty: Intermediate
---

## Statement

### The problem, from first principles

`[01-rnn-cell-forward]` computed `h_next = tanh(x @ weight_ih.T + bias_ih + h_prev @ weight_hh.T + bias_hh)`, a composition of two linear transformations (`[03-dl-training/02-layers/02-linear-backward]` already derived the backward rule for exactly this kind of operation) followed by a `tanh` nonlinearity. This question chains those two known backward rules together: first backpropagate through `tanh`, then feed the result into TWO separate applications of the linear-layer backward rule, one for the input-to-hidden path, one for the hidden-to-hidden path.

The `tanh` backward rule has a genuinely convenient property worth calling out directly: `d/dz tanh(z) = 1 - tanh(z)^2`, expressed entirely in terms of `tanh(z)`'s OWN output, not the original input `z`. Since the forward pass already computed and returned `h_next = tanh(z)`, the backward pass never needs to re-derive or re-access `z` at all, `1 - h_next**2` is directly computable from the SAVED forward output alone, a common and genuinely useful pattern (several other activation functions, like sigmoid, share this same "derivative expressible via the output" property).

### From theory to code

Implement `rnn_cell_backward(grad_h, h_next, x, h_prev, weight_ih, weight_hh)`. First, backpropagate through `tanh`: `grad_z = grad_h * (1 - h_next**2)`. Then apply `[03-dl-training/02-layers/02-linear-backward]`'s `linear_backward` LOGIC twice with this same `grad_z`: once treating `x`/`weight_ih` as the linear layer's input/weight (producing `grad_x`, `grad_weight_ih`, `grad_bias_ih`), and once treating `h_prev`/`weight_hh` as the linear layer's input/weight (producing `grad_h_prev`, `grad_weight_hh`, `grad_bias_hh`).

### Constraints

- `grad_z` must be computed via `grad_h * (1 - h_next**2)`, using the ALREADY-COMPUTED forward output `h_next`, never recomputing `tanh` or its argument from scratch.
- `grad_x = grad_z @ weight_ih` and `grad_h_prev = grad_z @ weight_hh` (the SAME `grad_z`, applied through each path's own weight matrix).
- `grad_weight_ih = grad_z.T @ x` and `grad_weight_hh = grad_z.T @ h_prev` (again, the same `grad_z`, transposed and matrix-multiplied against each path's own input).
- `grad_bias_ih` and `grad_bias_hh` are BOTH `grad_z.sum(axis=0)`, the SAME sum (since both biases were added to the SAME pre-activation `z`, each receives the identical gradient).

### Hints

<details>
<summary>Hint 1: The tanh backward step</summary>

`grad_z = grad_h * (1.0 - h_next**2)`. This is elementwise: `1 - tanh(z)^2` is `tanh`'s own derivative formula, and since `h_next` already equals `tanh(z)`, no separate computation of `z` is needed.

</details>

<details>
<summary>Hint 2: Reusing linear_backward's formulas, twice</summary>

For the input path: `grad_x = grad_z @ weight_ih`, `grad_weight_ih = grad_z.T @ x`, `grad_bias_ih = grad_z.sum(axis=0)`. For the hidden path: `grad_h_prev = grad_z @ weight_hh`, `grad_weight_hh = grad_z.T @ h_prev`, `grad_bias_hh = grad_z.sum(axis=0)`, exactly the SAME three formulas from `[03-dl-training/02-layers/02-linear-backward]`, applied with `(x, weight_ih)` in one call and `(h_prev, weight_hh)` in the other.

</details>

<details>
<summary>Hint 3</summary>

Return all six gradients in the exact order the function signature promises: `(grad_x, grad_h_prev, grad_weight_ih, grad_weight_hh, grad_bias_ih, grad_bias_hh)`.

</details>

## Theory

### The simple version

A single traffic light controlling two merging lanes at once, one lane feeding in NEW traffic (the current input `x`), one lane feeding in traffic that's been CIRCLING BACK from earlier (the previous hidden state `h_prev`). Both lanes merge into the SAME light (the shared pre-activation `z`, and its gradient `grad_z`), so any signal about how to adjust the light (the upstream gradient) has to flow back out to BOTH lanes it originally came from, `x`'s own path and `h_prev`'s own path, each independently, using the exact same merged signal.

### The formula

```
grad_z = grad_h * (1 - h_next^2)              # tanh backward, using SAVED output

grad_x          = grad_z @ weight_ih
grad_weight_ih  = grad_z.T @ x
grad_bias_ih    = sum over batch of grad_z

grad_h_prev     = grad_z @ weight_hh
grad_weight_hh  = grad_z.T @ h_prev
grad_bias_hh    = sum over batch of grad_z
```

### How PyTorch actually implements this

When you call `loss.backward()` on a model using `torch.nn.RNNCell` (or the full `torch.nn.RNN`, which chains many of these cells together across a sequence), PyTorch's autograd engine computes exactly these six gradients automatically, via a fused kernel rather than the two separate `linear_backward`-style calls used here for clarity. `Backprop through time (BPTT)`, immediately following this question, is precisely what happens when THIS single cell's backward pass gets chained across many time steps: `grad_h_prev` computed HERE becomes the `grad_h` argument fed into THIS SAME function again for the PREVIOUS time step, recursively walking backward through the whole sequence, exactly the same "gradient flows back through a chain, compounding at every step" structure `[03-dl-training/05-why-deep-networks-work/03-vanishing-exploding-gradients]`'s `matrix_gradient_norms` demonstrated for depth, except here the "depth" being multiplied through is the SEQUENCE LENGTH, and the SAME `weight_hh` matrix gets reused (and re-multiplied into the gradient) at every single one of those steps.

## Explanation

`rnn_cell_backward` first computes `grad_z = grad_h * (1 - h_next**2)`, applying `tanh`'s derivative (expressed via its own saved output, `h_next`) to the upstream gradient, giving the gradient with respect to the pre-activation sum `z = x @ weight_ih.T + bias_ih + h_prev @ weight_hh.T + bias_hh`.

It then applies `[03-dl-training/02-layers/02-linear-backward]`'s three formulas TWICE with this same `grad_z`: once against `(x, weight_ih)` to get `(grad_x, grad_weight_ih, grad_bias_ih)`, and once against `(h_prev, weight_hh)` to get `(grad_h_prev, grad_weight_hh, grad_bias_hh)`, since both linear transformations fed into the SAME shared sum before `tanh` was applied, and so both receive the IDENTICAL `grad_z` as their own upstream gradient.
