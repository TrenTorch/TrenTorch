---
name: research-clip-by-norm
title: 'Gradient Clipping: Clipping by Norm'
tags: [research-papers, optimization, stability]
difficulty: Beginner
---

## Statement

### The problem, from first principles

Pascanu et al. (2013) observed that recurrent gradients can explode. Clipping the gradient norm to a threshold bounds the step while keeping its direction.

### From theory to code

Implement `clip_by_norm(g, threshold)`, rescaling the gradient only when it is too large.

### Constraints

- Gradients under the threshold pass through unchanged.

### Hints

<details>
<summary>Hint 1</summary>

If the norm exceeds the threshold, multiply the gradient by threshold over the norm.

</details>

## Theory

### The simple version

Clipping by norm keeps the direction, which matters because the direction still points downhill while the magnitude is capped.

### The formula

$$g \leftarrow g\cdot\min\!\left(1,\frac{\tau}{\lVert g\rVert}\right)$$

### How NumPy/PyTorch actually implements this

Deep learning frameworks provide this as `clip_grad_norm_`, applied after backward and before the optimizer step.

## Explanation

Hand case: norm 5 clipped to 1 gives [0.6, 0.8].
