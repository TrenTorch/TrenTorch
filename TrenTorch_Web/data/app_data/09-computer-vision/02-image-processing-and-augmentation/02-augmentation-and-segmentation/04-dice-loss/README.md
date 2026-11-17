---
name: vision-dice-loss
title: Dice Loss
tags: [computer-vision, segmentation, loss-functions]
difficulty: Intermediate
---

## Statement

### The problem, from first principles

In medical or satellite segmentation the object of interest often covers a tiny fraction of the pixels. A per-pixel cross-entropy loss is then dominated by the easy background, and a model that predicts "background everywhere" scores 99% accuracy and learns nothing. The **Dice coefficient** measures _overlap_ instead: twice the intersection divided by the sum of the two areas. It ranges from 0 (no overlap) to 1 (perfect), and the background does not enter it at all. As a loss we use `1 - Dice` computed on predicted probabilities (so it stays differentiable), and a small `eps` keeps the ratio defined when both masks are empty.

### From theory to code

Implement `dice_coefficient` and `dice_loss`.

### Constraints

- `pred` holds probabilities in `[0, 1]` and `target` holds 0/1 labels, both of shape `(N, H, W)`.
- `dice_coefficient(pred, target, eps)` computes, **per sample**, `(2 * sum(pred * target) + eps) / (sum(pred) + sum(target) + eps)` over the spatial dimensions and returns the `(N,)` array.
- `dice_loss(pred, target, eps=1e-6)` is `1 - mean(dice_coefficient(...))` as a Python float.

### Hints

<details>
<summary>Hint 1</summary>

Reshape to `(N, -1)` and reduce over axis 1.

</details>

<details>
<summary>Hint 2</summary>

When both masks are empty, `eps` in numerator and denominator makes the coefficient exactly 1.

</details>

## Theory

### The simple version

Two translucent stencils laid over each other: Dice is how much of the combined stencil area is shared. Predicting nothing when there is something scores zero, however big the background.

### The formula

$$
\text{Dice} = \frac{2\sum_i p_i t_i + \epsilon}{\sum_i p_i + \sum_i t_i + \epsilon}, \qquad \mathcal{L}_{\text{Dice}} = 1 - \text{Dice}
$$

For binary masks Dice equals $2\,\text{IoU}/(1 + \text{IoU})$, so they rank predictions identically.

### How this is done in practice

MONAI, segmentation_models_pytorch and nnU-Net use Dice loss, usually combined with cross-entropy. The soft Dice here is differentiable in the probabilities, unlike thresholded overlap metrics.

## Explanation

Per-sample overlap computed with two sums and a product. The tests include the degenerate cases that make the epsilon necessary.
