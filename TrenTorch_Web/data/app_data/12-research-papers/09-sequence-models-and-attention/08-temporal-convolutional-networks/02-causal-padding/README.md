---
name: research-tcn-causal-padding
title: 'TCN: Causal Padding'
tags: [research-papers, sequence-models, convolution, sequence]
difficulty: Beginner
---

## Statement

### The problem, from first principles

A causal convolution must not look at future samples. Padding on the left by the dilated kernel span keeps the output length equal to the input and keeps the output causal.

### From theory to code

Implement `causal_padding(kernel, dilation)`, the left padding for a causal dilated convolution.

### Constraints

- Pad on the left only.

### Hints

<details>
<summary>Hint 1</summary>

Multiply kernel minus one by the dilation.

</details>

## Theory

### The simple version

The padding is the amount of past the dilated kernel reaches, so the output at each time uses exactly the samples at or before it.

### The formula

$$p = (k - 1)\,d$$

### How NumPy/PyTorch actually implements this

TCN layers apply this left padding before each dilated convolution.

## Explanation

Causal padding keeps the sequence length fixed across layers, which simplifies residual connections.
