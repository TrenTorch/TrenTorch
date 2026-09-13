---
name: dl-core-softmax
title: Softmax fwd/bwd
tags: [deep-learning, activations, autograd]
difficulty: Intermediate
---

## Statement

### The problem, from first principles

Every activation earlier in this track (`01-relu`, `02-sigmoid`, `03-tanh`) is elementwise: each output value depends only on its own corresponding input value. Softmax breaks that pattern on purpose — a classifier's raw scores ("logits") only make sense as _relative_ confidences, so turning them into a proper probability distribution requires every output to depend on every input, sharing one normalizing denominator across the whole row.

### From theory to code

`01-classical-ml/02-classification/06-softmax-cce`'s `softmax` already computed this forward pass. This question keeps that forward pass (normalizing over the last axis, like `torch.softmax(x, dim=-1)`) and adds `softmax_backward(grad_output, output)`, which takes `output` (the saved forward result), same pattern as `02-sigmoid`/`03-tanh`, and returns the vector-Jacobian product for the whole row at once — not a simple elementwise product, since softmax itself isn't elementwise.

### Constraints

- `x`: shape `(..., n_classes)`. `softmax_forward` returns the same shape, each row summing to `1`.
- `softmax_forward` must stay finite for large `|x|` (no overflow from a raw `exp`).
- `softmax_backward(grad_output, output)` takes the forward pass's own saved result, not the original `x`, and returns a same-shape gradient computed per row (reducing across the last axis, not elementwise).
- No Python loops; no mutating the inputs.

### Hints

Open one at a time. Each gives away a little more than the last.

<details>
<summary>Hint 1</summary>

Softmax isn't elementwise, so its backward pass can't be `grad_output * f'(x)` the way relu/sigmoid/tanh's are — every output in the row is coupled to every other output through the shared normalization.

</details>

<details>
<summary>Hint 2</summary>

The vector-Jacobian product collapses to `output * (grad_output - dot)`, where `dot` is a single per-row scalar: the sum of `grad_output * output` across the row.

</details>

## Theory

### The simple version

Because every output in a softmax row shares one denominator, nudging any single input logit doesn't just change its own probability — it very slightly redistributes probability mass across every other class in the row too, since they all have to keep summing to `1`. The backward pass has to account for that shared redistribution, which is exactly what makes it structurally different from an elementwise activation's backward pass.

### The formula

```text
softmax(x)_i = exp(x_i) / sum_j(exp(x_j))
```

Two things distinguish it from every other activation in this track. First, it is **not elementwise**: `softmax(x)_i` depends on every `x_j`, not just `x_i`, because they all share one normalizing denominator. Second, its numerically stable computation subtracts the row max before exponentiating:

```text
softmax(x)_i = exp(x_i - max(x)) / sum_j(exp(x_j - max(x)))
```

This is mathematically identical to the plain formula (the `-max(x)` term cancels between numerator and denominator) but avoids `exp` overflowing on large inputs — `exp(1000)` is `inf` in float64, `exp(1000 - 1000) = exp(0) = 1` is fine.

Because softmax mixes every input into every output, its backward pass is not `grad_output * f'(x)` the way relu/sigmoid/tanh's are. The full Jacobian of softmax is a dense matrix (`d(softmax_i)/d(x_j)` is nonzero for every `i, j` pair), but the vector-Jacobian product a real backward pass needs collapses to a clean closed form:

```text
dL/dx_i = output_i * (grad_output_i - sum_j(grad_output_j * output_j))
```

This is the same reduce-then-broadcast shape used throughout deep learning whenever a layer's outputs are coupled by a shared normalization (batch norm and layer norm's backward passes have the same structural shape).

### How PyTorch actually implements this

Context only, untested by your submission: `torch.softmax(x, dim=-1)` computes the same stable, max-subtracted forward pass, and PyTorch's autograd derives exactly this reduce-then-broadcast vector-Jacobian product for the backward pass — the same formula this exercise implements by hand, generalized across whichever axis `dim` names.

## Explanation

`softmax_forward` shifts by the row max (`np.max(..., axis=-1, keepdims=True)`), exponentiates, and divides by the row sum, exactly the stable formula from Theory. `keepdims=True` keeps broadcasting correct against the original shape.

`softmax_backward` computes `dot = sum(grad_output * output, axis=-1, keepdims=True)` (the `sum_j(grad_output_j * output_j)` term, one scalar per row) and returns `output * (grad_output - dot)`, the closed-form vector-Jacobian product from Theory, applied per row via broadcasting.
