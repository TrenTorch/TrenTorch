---
name: research-tcn-receptive-field
title: 'TCN: Receptive Field'
tags: [research-papers, sequence-models, convolution, sequence]
difficulty: Intermediate
---

## Statement

### The problem, from first principles

Temporal convolutional networks (Bai et al., 2018) use causal convolutions with exponentially growing dilations. The receptive field grows exponentially with depth, so long histories are covered without recurrence.

### From theory to code

Implement `tcn_receptive_field(kernel, levels)`, the receptive field of the stack.

### Constraints

- Dilation at level i is two to the i.

### Hints

<details>
<summary>Hint 1</summary>

Sum (kernel minus one) times the dilation over the levels, which is a geometric series, then add one.

</details>

## Theory

### The simple version

A TCN has no recurrence, so it trains in parallel across time while still covering long context.

### The formula

$$R = 1 + (k - 1)\sum_{i=0}^{L-1}2^i = 1 + (k-1)(2^L - 1)$$

### How NumPy/PyTorch actually implements this

TCN implementations choose the number of levels so that the receptive field covers the needed history.

## Explanation

The closed form uses the geometric series; the explicit sum in the last test is the same quantity.
