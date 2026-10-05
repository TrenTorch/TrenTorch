---
name: research-lars-update
title: 'LARS: The Layer-wise Update'
tags: [research-papers, optimization, large-batch]
difficulty: Intermediate
---

## Statement

### The problem, from first principles

After computing a layer's trust ratio, LARS scales the global learning rate by it and applies the decayed gradient. Every layer moves a comparable relative amount, even when their gradient magnitudes differ widely.

### From theory to code

Implement `lars_update(w, g, lr, eta, wd)`, one LARS step for a single layer.

### Constraints

- Use the trust ratio from the previous question.

### Hints

<details>
<summary>Hint 1</summary>

Compute the trust ratio, multiply it with lr, then subtract that times the decayed gradient from the weights.

</details>

## Theory

### The simple version

Scaling by the trust ratio is the mechanism that lets learning rates grow with batch size without the early layers diverging.

### The formula

$$w \leftarrow w - \eta\,\lambda_\ell\,(\nabla L + \beta w)$$

### How NumPy/PyTorch actually implements this

Large-batch BERT and ResNet recipes use this per-layer step.

## Explanation

Hand case: the trust ratio is 2.5, so the step is 0.25 times the gradient, giving [2.85, 3.8].
