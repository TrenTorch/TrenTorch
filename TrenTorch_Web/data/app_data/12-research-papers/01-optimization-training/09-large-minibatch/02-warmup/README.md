---
name: research-goyal-warmup
title: 'Large Minibatch SGD: Gradual Warmup'
tags: [research-papers, optimization, large-batch]
difficulty: Beginner
---

## Statement

### The problem, from first principles

Goyal et al. also warm up the large learning rate gradually. Starting from a small rate and ramping up over the first few epochs avoids early divergence when the scaled rate is high.

### From theory to code

Implement `gradual_warmup_lr(target, t, warmup)`, the linear ramp to the target then hold.

### Constraints

- Steps are numbered from one.

### Hints

<details>
<summary>Hint 1</summary>

Multiply the target by the smaller of one and the step over the warmup length.

</details>

## Theory

### The simple version

Early in training the weights change quickly, so a large rate applied at once can diverge; ramping keeps the first steps small.

### The formula

$$\eta_t = \eta_{\text{target}}\cdot\min\!\left(1,\frac{t}{T_{\text{warm}}}\right)$$

### How NumPy/PyTorch actually implements this

Training schedulers implement this as a linear warmup phase before the main decay.

## Explanation

Hand case: at step 2 of 4 the rate is half the target, 0.2.
