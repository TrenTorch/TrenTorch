---
name: lm-steering-vectors
title: Steering Vectors
tags: [interpretability, activation-steering, residual-stream]
difficulty: Intermediate
---

## Statement

### The problem, from first principles

If a hidden state contains a direction that encodes a concept, you can push the model along that direction and change its behavior without any training. The standard recipe finds the direction from contrast pairs. Run the model on prompts that show the concept and on matching prompts that do not, record the residual stream at some layer, and take the **difference of the mean activations**. Adding a multiple of that vector to the residual stream at inference time steers generation toward the concept, and subtracting it steers away. The multiplier controls strength: too small does nothing and too large breaks fluency.

### From theory to code

Implement `steering_vector` and `apply_steering`.

### Constraints

- `pos_acts` and `neg_acts` are `(n, d)` and `(m, d)` activation arrays from contrast prompts. `steering_vector(pos_acts, neg_acts, normalize)` returns `mean(pos) - mean(neg)`, divided by its L2 norm when `normalize=True` (and left alone if the norm is zero).
- `apply_steering(resid, v, alpha, positions=None)` returns a copy of `resid` (shape `(T, d)`) with `alpha * v` added at the listed token positions, or at all positions when `positions is None`.
- The input `resid` must not be modified.
- `positions` is a list of integer indices.

### Hints

<details>
<summary>Hint 1</summary>

Slice assignment on a copy: `out[positions] += alpha * v` works for a list of positions without repeats.

</details>

<details>
<summary>Hint 2</summary>

Normalizing makes `alpha` comparable between layers whose activations have different scales.

</details>

## Theory

### The simple version

Imagine a dial in the model's head labelled "formal vs casual". Averaging the model's state over formal sentences and over casual ones and subtracting gives the direction of the dial. Turning it is just adding the direction.

### The formula

$$
v = \frac{\bar h_{+} - \bar h_{-}}{\lVert \bar h_{+} - \bar h_{-}\rVert}, \qquad h'_t = h_t + \alpha\, v
$$

The projection of any activation onto $v$, $h^\top v$, is a one-number readout of how strongly the concept is present, so steering and probing are two sides of one idea.

### How this is done in practice

Methods such as activation addition and representation engineering implement this with forward hooks (`register_forward_hook` in PyTorch) that add the vector at a chosen layer. Layer choice, the set of token positions and `alpha` are all tuned empirically, usually on a held-out behavioral metric.

## Explanation

The vector is the difference between two centroids and the application is a masked addition. Because addition on a copy touches only the requested positions, the same vector can steer only the prompt, only the generated tokens, or everything.
