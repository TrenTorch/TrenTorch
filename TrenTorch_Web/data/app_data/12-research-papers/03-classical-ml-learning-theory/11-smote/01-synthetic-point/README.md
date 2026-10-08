---
name: research-smote-point
title: 'SMOTE: Interpolating Between Two Points'
tags: [research-papers, classical-ml, imbalance, smote]
difficulty: Beginner
---

## Statement

### The problem, from first principles

SMOTE (Chawla et al., 2002) fights class imbalance by creating new minority-class examples. Each new point lies between a real minority sample and one of its neighbors, so the synthetic data stays inside the minority region.

### From theory to code

Implement `smote_point(x, neighbor, u)`, returning the point a fraction `u` of the way from `x` to `neighbor`.

### Constraints

- `u` is between 0 and 1.

### Hints

<details>
<summary>Hint 1</summary>

Start at `x` and step `u` times the vector to the neighbor.

</details>

## Theory

### The simple version

Interpolation fills gaps between existing points rather than copying them, so the classifier sees more varied minority examples.

### The formula

$$x_{\text{new}} = x_i + u\,(x_{\text{nn}} - x_i), \qquad u \sim \text{Uniform}(0, 1)$$

### How NumPy/PyTorch actually implements this

`imblearn.over_sampling.SMOTE` performs the same interpolation, with neighbors found by a k-d tree.

## Explanation

The synthetic point is a convex combination of two minority samples, so it stays within their span.
