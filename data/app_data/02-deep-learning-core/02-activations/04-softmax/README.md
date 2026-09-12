---
name: dl-core-softmax
title: Softmax fwd/bwd
tags: [deep-learning, activations, autograd]
difficulty: Intermediate
---

## Statement

Implement:

```python
def softmax_forward(x) -> np.ndarray: ...
def softmax_backward(grad_output, output) -> np.ndarray: ...
```

- `softmax_forward` normalizes over the last axis (like `torch.softmax(x, dim=-1)`), turning a row of raw scores into a probability distribution that sums to `1`.
- `softmax_backward` takes `output` (the saved forward result), same pattern as `02-sigmoid`/`03-tanh`, and returns the vector-Jacobian product for the whole row at once.

## Theory

Softmax turns a vector of arbitrary real-valued scores ("logits") into a probability distribution:

```text
softmax(x)_i = exp(x_i) / sum_j(exp(x_j))
```

Two things distinguish it from every other activation in this track. First, it is **not elementwise**: `softmax(x)_i` depends on every `x_j`, not just `x_i`, because they all share one normalizing denominator. Second, its numerically stable computation subtracts the row max before exponentiating:

```text
softmax(x)_i = exp(x_i - max(x)) / sum_j(exp(x_j - max(x)))
```

This is mathematically identical to the plain formula (the `-max(x)` term cancels between numerator and denominator) but avoids `exp` overflowing on large inputs, `exp(1000)` is `inf` in float64, `exp(1000 - 1000) = exp(0) = 1` is fine.

Because softmax mixes every input into every output, its backward pass is not `grad_output * f'(x)` the way relu/sigmoid/tanh's are. The full Jacobian of softmax is a dense matrix (`d(softmax_i)/d(x_j)` is nonzero for every `i, j` pair), but the vector-Jacobian product a real backward pass needs collapses to a clean closed form:

```text
dL/dx_i = output_i * (grad_output_i - sum_j(grad_output_j * output_j))
```

This is the same reduce-then-broadcast shape used throughout deep learning whenever a layer's outputs are coupled by a shared normalization (batch norm and layer norm's backward passes have the same structural shape).

## Explanation

`softmax_forward` shifts by the row max (`np.max(..., axis=-1, keepdims=True)`), exponentiates, and divides by the row sum, exactly the stable formula from Theory. `keepdims=True` keeps broadcasting correct against the original 2D shape.

`softmax_backward` computes `dot = sum(grad_output * output, axis=-1, keepdims=True)` (the `sum_j(grad_output_j * output_j)` term, one scalar per row) and returns `output * (grad_output - dot)`, the closed-form vector-Jacobian product from Theory, applied per row via broadcasting.
