---
name: research-gptq-error
title: 'GPTQ: Measuring Quantization Error'
tags: [research-papers, systems, quantization, inference]
difficulty: Intermediate
---

## Statement

### The problem, from first principles

Comparing quantized and original weights is the basic check of a quantization scheme. The mean absolute error summarizes how far the rounded weights are from the originals.

### From theory to code

Implement `quantization_error(x, bits)`, the mean absolute error of symmetric quantization.

### Constraints

- Returns a float.

### Hints

<details>
<summary>Hint 1</summary>

Quantize and dequantize as in the previous questions, then average the absolute differences.

</details>

## Theory

### The simple version

More bits give a finer grid and smaller error. The error an individual layer introduces is what GPTQ tries to minimize, since small per-layer errors compound through the network.

### The formula

$$\text{MAE} = \frac{1}{n}\sum_i |x_i - \hat x_i|$$

### How NumPy/PyTorch actually implements this

Quantization reports compare this error across bit widths for each layer.

## Explanation

The error on a uniform grid is at most half a step; this function measures the realized value on actual weights.
