---
name: research-rope-relative-dot
title: 'RoFormer: The Dot Product Depends Only on Relative Position'
tags: [research-papers, transformers, llm, position, rope]
difficulty: Advanced
---

## Statement

### The problem, from first principles

The point of RoPE is that attention scores should depend on how far apart two tokens are, not on their absolute positions. Rotating queries and keys by their own positions gives exactly that: the product of two rotations depends only on the difference of the angles.

### From theory to code

Implement `rope_dot(q, k, m, n, base)`, which rotates the query to position `m`, the key to position `n`, and returns their dot product.

### Constraints

- Equal positions reduce to the ordinary dot product.

### Hints

<details>
<summary>Hint 1</summary>

Reuse the rotation from `rope_rotate` for each vector, then take a dot product.

</details>

## Theory

### The simple version

A 2D rotation by `a` followed by the transpose of a rotation by `b` is a rotation by `a - b`. So the score only depends on `m - n`, which is the relative position.

### The formula

$$\langle R_m q, R_n k\rangle = \langle R_{m-n} q, k\rangle$$

### How NumPy/PyTorch actually implements this

Long-context models rely on this property to generalize to longer sequences than seen in training.

## Explanation

The rotation matrices are orthogonal, which is why the relative form follows directly. This property is what the paper proves for RoPE.
