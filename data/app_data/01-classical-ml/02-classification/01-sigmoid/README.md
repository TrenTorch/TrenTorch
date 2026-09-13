---
name: classification-sigmoid
title: Sigmoid Function
tags: [classical-ml, classification, activations]
difficulty: Beginner
---

## Statement

### The problem, from first principles

A linear score can be any real number, but a binary prediction needs a value that can be read as confidence for one of two outcomes. Sigmoid converts scores to that probability-like scale while retaining their ordering. This implementation also has to survive scores too extreme for a direct exponential.

### From theory to code

Implement `sigmoid(z)` elementwise. Theory gives the transform; the implementation first bounds the input so its exponential remains finite.

### Constraints

- `z` may have any NumPy array shape; preserve that shape.
- Return a finite numeric array that is monotonic in `z`.
- Return `0.5` for zero.
- Clip `z` to `[-500, 500]` before exponentiating.
- Do not use Python loops or mutate the caller's array.

### Hints

Open one at a time. Each gives away a little more than the last.

<details><summary>Hint 1</summary>

The transform is applied independently to every element, so NumPy already provides the iteration.

</details>

<details><summary>Hint 2</summary>

Clamp the raw scores before using the exponential; a negative raw score becomes a positive exponent argument.

</details>

## Theory

### The simple version

Sigmoid is a soft switch: strongly negative evidence is close to off, strongly positive evidence is close to on, and no evidence sits exactly halfway.

### The formula

```text
z_safe = clip(z, -500, 500)
sigmoid(z) = 1 / (1 + exp(-z_safe))
```

The clip protects `exp(-z_safe)` from overflow while leaving the saturated behavior of extreme scores intact.

### How PyTorch actually implements this

Context only, untested by your submission: `torch.sigmoid` applies the corresponding elementwise activation. This exercise specifies its NumPy clipping strategy explicitly.

## Explanation

`z = np.clip(z, -500, 500)` deliberately rebinds a clipped array instead of mutating the caller. `np.exp(-z)` then never receives an argument above 500, so the return expression stays finite even for inputs such as `-1e5`. NumPy applies both operations elementwise, preserving the original shape.
