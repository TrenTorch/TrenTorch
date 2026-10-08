---
name: research-gptq-dequantize
title: 'GPTQ: Dequantizing Weights'
tags: [research-papers, systems, quantization, inference]
difficulty: Beginner
---

## Statement

### The problem, from first principles

Inference with a quantized model multiplies the stored integer codes by a scale to recover approximate weights, usually inside the matrix kernel. Dequantization is that multiplication.

### From theory to code

Implement `dequantize(q, scale)`, returning the approximate float weights.

### Constraints

- Return floats.

### Hints

<details>
<summary>Hint 1</summary>

Multiply the integer codes by the scale.

</details>

## Theory

### The simple version

The rounding error of this round trip is at most half a scale step per weight, which bounds how much the model's behaviour can change.

### The formula

$$\hat x = s\,q$$

### How NumPy/PyTorch actually implements this

Quantized inference kernels fuse this scaling into the matrix product so the float weights never fully materialize.

## Explanation

The round trip error bound follows from rounding to the nearest code on a uniform grid of spacing s.
