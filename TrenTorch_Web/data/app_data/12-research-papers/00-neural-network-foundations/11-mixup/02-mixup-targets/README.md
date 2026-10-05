---
name: research-mixup-targets
title: 'Mixup: Blending the Labels'
tags: [research-papers, augmentation, mixup]
difficulty: Beginner
---

## Statement

### The problem, from first principles

Mixup mixes labels exactly as it mixes inputs, so a blended example gets a soft target. The model is then trained to match that soft label, not a hard one.

### From theory to code

Implement `mixup_targets(y, perm, lam)`, applying the same permutation and weight to the one-hot labels.

### Constraints

- Each output row sums to 1 when the input rows do.

### Hints

<details>
<summary>Hint 1</summary>

Use the same expression as the inputs, applied to the label matrix.

</details>

## Theory

### The simple version

If an input is 70% class A and 30% class B, its target is the same 70/30 mix. Training on soft targets is what makes the approach work.

### The formula

$$\tilde y = \lambda\, y_i + (1 - \lambda)\, y_{\pi(i)}$$

### How NumPy/PyTorch actually implements this

Training uses cross-entropy against these soft targets directly; no special loss is needed.

## Explanation

Blending one-hot rows gives a valid probability distribution, because a convex combination of distributions is still one.
