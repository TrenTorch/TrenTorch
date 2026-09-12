---
name: dl-training-linear-backward
title: Linear bwd
tags: [neural-networks, layers, autograd]
difficulty: Intermediate
---

## Statement

### The problem, from first principles

`[01-linear-forward]` computed `y = x @ weight.T + bias`. To actually train a network, gradient descent needs to know how a small change in each of `x`, `weight`, and `bias` would change the final loss, given only the gradient of the loss with respect to `y` (the "upstream gradient," handed down from whatever layer comes after this one). `[02-deep-learning-core/04-autograd]`'s `matmul_backward` already derived the general rule for backpropagating through a matrix multiplication; this question applies that exact rule to the specific shapes a linear layer uses.

Three different gradients are needed here, for three different reasons: `grad_x` is needed so the PREVIOUS layer can continue backpropagating further back through the network; `grad_weight` and `grad_bias` are needed directly by the optimizer (every optimizer question in this Part, `sgd_step`, `adam_step`, and so on, consumes exactly a gradient like this one) to actually update this layer's own learnable parameters.

### From theory to code

Implement `linear_backward(grad_output, x, weight)`, returning the three gradients `(grad_x, grad_weight, grad_bias)`. `grad_output` has the same shape as the forward pass's output, `(batch_size, out_features)`. Each of the three return values must have the SAME shape as the corresponding forward-pass input it's a gradient with respect to: `grad_x` matches `x`'s shape, `grad_weight` matches `weight`'s shape, `grad_bias` matches `bias`'s shape.

### Constraints

- `grad_x` must have the same shape as `x`: `(batch_size, in_features)`.
- `grad_weight` must have the same shape as `weight`: `(out_features, in_features)`.
- `grad_bias` must have the same shape as `bias`: `(out_features,)`, summed (not averaged) across the batch dimension.
- Do not use any deep learning framework's autograd; derive and implement the gradients directly.

### Hints

<details>
<summary>Hint 1: grad_x</summary>

`y = x @ weight.T`, so by the matmul backward rule (`[02-deep-learning-core/04-autograd/03-backward-matmul]`'s `matmul_backward`, with `a = x` and `b = weight.T`), `grad_x = grad_output @ weight` (since `(weight.T).T = weight`).

</details>

<details>
<summary>Hint 2: grad_weight</summary>

By the same matmul backward rule, the gradient with respect to `weight.T` is `x.T @ grad_output`, which has shape `(in_features, out_features)`. Since `weight` is the TRANSPOSE of `weight.T`, transpose that result: `grad_weight = grad_output.T @ x`, giving the correct `(out_features, in_features)` shape directly.

</details>

<details>
<summary>Hint 3: grad_bias</summary>

The forward pass added the SAME `bias` vector to every row of the batch, so by the multivariable chain rule, `bias`'s total gradient is the SUM of the upstream gradient across every row of the batch it was added to: `grad_output.sum(axis=0)`.

</details>

## Theory

### The simple version

If you added the same fixed delivery fee to every customer's order total, and you learned the total profit went up by some amount, that increase is the COMBINED effect of the fee across every single order, not just one: to find how much credit the fee itself deserves, you sum its contribution across every order it was added to. `grad_bias` works exactly this way: `bias` was added identically to every row of the batch, so its gradient is the sum of the upstream gradient across all of those rows.

### The formula

With `grad_output` shape `(batch_size, out_features)`, `x` shape `(batch_size, in_features)`, `weight` shape `(out_features, in_features)`:

```
grad_x      = grad_output @ weight               # (batch_size, in_features)
grad_weight = grad_output.T @ x                   # (out_features, in_features)
grad_bias   = sum over batch_size of grad_output  # (out_features,)
```

Every one of these three formulas comes directly from applying the chain rule to `y = x @ weight.T + bias`, treating the matmul and the bias-add as two operations composed together, exactly the way `[02-deep-learning-core/04-autograd]`'s `Value` graph would trace it if `x`, `weight`, and `bias` were all wrapped as graph nodes.

### How PyTorch actually implements this

When you call `loss.backward()` on a model built from `nn.Linear`, PyTorch's autograd engine calls a fused CPU/CUDA kernel (`AddmmBackward0` in the autograd graph, visible if you print `out.grad_fn`) that computes exactly these three formulas as a single fused operation, for the same reason `nn.functional.linear`'s forward pass fuses the matmul and bias-add: avoiding materializing intermediate tensors. `weight.grad` and `bias.grad` accumulate into the `.grad` attribute of each `nn.Parameter` (using `+=` semantics, which is why `optimizer.zero_grad()` must be called before each new `backward()`, otherwise gradients from the previous step silently accumulate on top). `grad_x` is what actually flows backward into whatever produced `x`, continuing the chain all the way back to the model's input, exactly the recursive structure `[02-deep-learning-core/04-autograd/06-minimal-autograd-engine]`'s `backward` function walks through its topological order.

## Explanation

`grad_x = grad_output @ weight` applies the matmul backward rule to `y = x @ weight.T`: since one factor of the forward matmul was `weight.T`, the gradient flowing back to the OTHER factor (`x`) is `grad_output @ (weight.T).T = grad_output @ weight`.

`grad_weight = grad_output.T @ x` applies the same rule from the other side: the gradient flowing back to `weight.T` is `x.T @ grad_output`, and transposing that (since `weight` is the transpose of `weight.T`) gives `grad_output.T @ x` directly in the correct `(out_features, in_features)` shape.

`grad_bias = grad_output.sum(axis=0)` sums the upstream gradient across the batch dimension, reflecting that the same `bias` vector was added to every row during the forward pass.
