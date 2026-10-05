---
name: vision-total-variation
title: Total Variation Regularization
tags: [computer-vision, style-transfer, regularization, image-priors]
difficulty: Beginner
---

## Statement

### The problem, from first principles

Optimizing the pixels of an image to match feature statistics tends to produce high-frequency noise: speckles that fool the network's features but look bad to a person. Real images are mostly **piecewise smooth**, with neighbouring pixels similar except at edges. **Total variation** (TV) penalizes the differences between neighbouring pixels, so adding it to the loss acts as a prior toward clean images. The L1 form used here punishes noise but still allows sharp edges to survive better than a squared penalty, which would blur them. It is the same idea as a denoising prior and is a standard regularizer for any pixel-space optimization.

### From theory to code

Implement `total_variation`.

### Constraints

- `img` has shape `(C, H, W)` or `(H, W)`; always work on the last two axes.
- Return `0.5 * (mean(|img[..., 1:, :] - img[..., :-1, :]|) + mean(|img[..., :, 1:] - img[..., :, :-1]|))` as a float: the average absolute vertical difference plus the average absolute horizontal difference, halved.

### Hints

<details>
<summary>Hint 1</summary>

Use slicing on the last two axes with `...` so one function handles both shapes.

</details>

<details>
<summary>Hint 2</summary>

A constant image has zero total variation and an image of pure noise has a large one.

</details>

## Theory

### The simple version

Running a finger over a surface: a smooth wall gives little change, a gravel path gives a lot. The penalty is the average roughness.

### The formula

$$
\text{TV}(x) = \tfrac12\Big(\operatorname{mean}|x_{i+1,j} - x_{i,j}| + \operatorname{mean}|x_{i,j+1} - x_{i,j}|\Big)
$$

### How this is done in practice

Style transfer, super-resolution and image inpainting pipelines all add a TV term, and the Rudin-Osher-Fatemi model made TV minimization a classical denoising method. In frameworks the loss is differentiable almost everywhere, so autograd handles it.

## Explanation

Two slices and two means. The tests contrast flat, ramp, noisy and edge images to show what the penalty rewards and punishes.
