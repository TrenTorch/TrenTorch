---
name: research-goyal-scaled-lr
title: 'Large Minibatch SGD: The Linear Scaling Rule'
tags: [research-papers, optimization, large-batch]
difficulty: Beginner
---

## Statement

### The problem, from first principles

Goyal et al. (2017) train with very large minibatches by scaling the learning rate linearly with the batch size. Doubling the batch doubles the step, since the gradient estimate is averaged over twice as many examples.

### From theory to code

Implement `scaled_lr(base_lr, batch, base_batch)`, the linearly scaled learning rate.

### Constraints

- Return the scaled rate as a number.

### Hints

<details>
<summary>Hint 1</summary>

Multiply the base learning rate by the ratio of the new batch size to the base batch size.

</details>

## Theory

### The simple version

With a bigger batch the gradient is less noisy, so a proportionally bigger step keeps the same progress per example seen.

### The formula

$$\eta_{\text{new}} = \eta_{\text{base}}\cdot\frac{B}{B_{\text{base}}}$$

### How NumPy/PyTorch actually implements this

The ImageNet recipe in the paper uses base 0.1 at batch 256, scaled to 8192 with this rule.

## Explanation

Hand case: 0.1 times 1024 over 256 is 0.4.
