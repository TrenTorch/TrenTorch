---
name: research-gptq-quantize
title: 'GPTQ: Symmetric Quantization'
tags: [research-papers, systems, quantization, inference]
difficulty: Intermediate
---

## Statement

### The problem, from first principles

GPTQ (Frantar et al., 2022) quantizes weights to a few bits after training. The simplest building block is symmetric round-to-nearest quantization: pick a scale from the largest weight, then round each weight to a small integer grid.

### From theory to code

Implement `quantize_symmetric(x, bits)`, returning integer codes and the scale.

### Constraints

- Use a scale of one when all weights are zero.

### Hints

<details>
<summary>Hint 1</summary>

Set the scale to the largest magnitude divided by the largest code, round the scaled weights, and clip to the code range.

</details>

## Theory

### The simple version

A symmetric grid keeps zero exactly representable and needs only one scale per tensor. GPTQ adds an error-correcting step on top of this rounding, which the next questions build toward.

### The formula

$$s = \frac{\max|x|}{2^{b-1}-1}, \qquad q = \operatorname{clip}\big(\operatorname{round}(x/s),\,-q_{\max},\,q_{\max}\big)$$

### How NumPy/PyTorch actually implements this

Quantization toolkits compute the same scale and codes per tensor or per group before packing the integers.

## Explanation

Rounding to the nearest code minimizes each weight's error independently; the paper's contribution is distributing the rounding error across the remaining weights.
