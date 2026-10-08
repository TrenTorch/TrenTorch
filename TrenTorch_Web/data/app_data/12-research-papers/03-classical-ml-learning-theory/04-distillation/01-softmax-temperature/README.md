---
name: research-distill-softmax-temperature
title: 'Distilling the Knowledge: Softmax With Temperature'
tags: [research-papers, classical-ml, distillation, knowledge]
difficulty: Beginner
---

## Statement

### The problem, from first principles

Hinton et al. (2015) observed that a large model's softmax is nearly one-hot, hiding how it ranks the wrong classes. Dividing the logits by a temperature T above 1 softens the distribution and exposes that ranking, which a smaller student can learn from.

### From theory to code

Implement `softmax_temperature(logits, T)`, returning the softmax of `logits / T`.

### Constraints

- `T` is positive.

### Hints

<details>
<summary>Hint 1</summary>

Divide by `T`, subtract the maximum for stability, exponentiate and normalize.

</details>

## Theory

### The simple version

A higher T makes the output closer to uniform, so the relative sizes of the wrong-class probabilities become visible. The student learns these soft targets, not just the hard label.

### The formula

$$q_i = \frac{\exp(z_i / T)}{\sum_j \exp(z_j / T)}$$

### How NumPy/PyTorch actually implements this

Distillation scripts call the same scaled softmax on teacher and student logits before computing the loss.

## Explanation

At T = 1 this is the usual softmax; the paper uses a larger T during distillation and then returns to T = 1 at test time.
