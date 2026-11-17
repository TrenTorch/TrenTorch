---
name: research-rope-rotate
title: 'RoFormer: Rotating a Vector by Position'
tags: [research-papers, transformers, llm, position, rope]
difficulty: Advanced
---

## Statement

### The problem, from first principles

A pair of features can be rotated in a plane. RoPE rotates each pair by an angle equal to the token's position times a fixed frequency, so every position is encoded directly in the geometry of the vectors.

### From theory to code

Implement `rope_rotate(x, pos, base)`, which rotates each consecutive pair of features by `pos * theta_i`.

### Constraints

- Pairs are `(x[0], x[1])`, `(x[2], x[3])`, and so on.

### Hints

<details>
<summary>Hint 1</summary>

Compute the angles from the frequencies, then apply a 2D rotation to each pair of even and odd indices.

</details>

## Theory

### The simple version

Rotation preserves length, so the position changes only the direction of the vector. Attention then sees position through the angle between query and key.

### The formula

$$\begin{pmatrix} x'_{2i} \\ x'_{2i+1} \end{pmatrix} = \begin{pmatrix} \cos m\theta_i & -\sin m\theta_i \\ \sin m\theta_i & \cos m\theta_i \end{pmatrix}\begin{pmatrix} x_{2i} \\ x_{2i+1} \end{pmatrix}$$

### How NumPy/PyTorch actually implements this

Hugging Face's Llama implementation applies this rotation with `rotate_half` and cosine/sine caches.

## Explanation

Each pair is a separate 2x2 rotation, applied with vectorized NumPy slices over the even and odd indices.
