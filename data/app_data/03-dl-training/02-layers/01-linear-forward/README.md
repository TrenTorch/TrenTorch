---
name: dl-training-linear-forward
title: Linear fwd
tags: [neural-networks, layers]
difficulty: Beginner
---

## Statement

### The problem, from first principles

Every neural network, no matter how large or how exotic its attention mechanisms or convolutions, is built out of one operation repeated over and over: a linear (fully connected / dense) transformation of its input, usually followed by a nonlinearity. Understanding what a "linear layer" actually computes, down to the exact shapes involved, is the foundation everything else in this Part builds on: `[02-layers/02-linear-backward]` needs this forward pass to differentiate, and the `Sequential` container you'll build later in this track needs to chain many of these together correctly.

A linear layer holds two learnable tensors: a weight matrix and a bias vector. Given an input vector, it computes a new vector where each output entry is a weighted sum of every input entry, plus a learned constant offset. Stacked into a batch of many input vectors at once (the normal case during training, for GPU efficiency), this becomes a single matrix multiplication.

### From theory to code

Implement `linear_forward(x, weight, bias)`. `x` has shape `(batch_size, in_features)`. Match PyTorch's own `nn.Linear` convention exactly: `weight` has shape `(out_features, in_features)` (each ROW of `weight` is the set of weights for one output neuron), not `(in_features, out_features)`. `bias` has shape `(out_features,)`. The output has shape `(batch_size, out_features)`.

### Constraints

- `weight` is `(out_features, in_features)`, matching `torch.nn.Linear.weight`'s shape exactly, not its transpose.
- The bias must broadcast correctly across the batch dimension: every row of the output gets the same bias vector added.
- Must work for any `batch_size`, including `batch_size == 1`.

### Hints

<details>
<summary>Hint 1</summary>

Since `weight` is `(out_features, in_features)` rather than `(in_features, out_features)`, you need `x @ weight.T`, not `x @ weight`, to get shapes that line up: `(batch_size, in_features) @ (in_features, out_features) = (batch_size, out_features)`.

</details>

<details>
<summary>Hint 2</summary>

`x @ weight.T + bias`: NumPy's broadcasting handles adding a `(out_features,)` vector to a `(batch_size, out_features)` matrix automatically, adding it to every row.

</details>

## Theory

### The simple version

A recipe that turns a list of ingredient QUANTITIES into a single predicted COST: multiply each ingredient's quantity by its own price-per-unit, add them all up, then add a fixed delivery fee. Each output neuron of a linear layer is its own such recipe, with its own set of "prices" (that output neuron's row of `weight`) and its own "delivery fee" (that output neuron's entry in `bias`), applied to the exact same input.

### The formula

For a single input vector `x` (length `in_features`) and a single output neuron `j`:

```
y_j = sum over i of (x_i * weight[j, i]) + bias[j]
```

Stacked across all `out_features` output neurons at once, and across a whole batch, this is:

```
Y = X @ weight.T + bias
```

where `X` is `(batch_size, in_features)`, `weight.T` is `(in_features, out_features)`, and the resulting `Y` is `(batch_size, out_features)`.

### How PyTorch actually implements this

`torch.nn.Linear.forward` calls `torch.nn.functional.linear(input, weight, bias)`, which dispatches to a fused ATen kernel (`addmm` under the hood for the 2D case) rather than computing the matmul and the bias-add as two separate operations: fusing them avoids materializing an intermediate tensor and is meaningfully faster on both CPU and GPU. The reason PyTorch stores `weight` as `(out_features, in_features)` rather than the mathematically more "natural" `(in_features, out_features)` is exactly so this fused `addmm` call can use `weight.T` without needing an actual memory copy: NumPy and PyTorch both implement `.T` as a zero-cost view (just swapped strides), so `x @ weight.T` is just as fast as `x @ weight` would be with the other layout. `weight` and `bias` are both `nn.Parameter` instances, meaning autograd tracks gradients through them automatically; `[02-layers/02-linear-backward]` implements exactly what that backward pass computes by hand.

## Explanation

`linear_forward` computes `x @ weight.T + bias` directly: `weight.T` reshapes `(out_features, in_features)` into `(in_features, out_features)` so the matrix multiplication's inner dimensions line up with `x`'s `(batch_size, in_features)`, producing a `(batch_size, out_features)` result, and NumPy's broadcasting adds the `(out_features,)` bias vector to every row of that result in one call.
