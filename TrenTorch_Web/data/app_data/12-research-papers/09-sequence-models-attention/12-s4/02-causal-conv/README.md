---
name: research-s4-causal-conv
title: 'S4: Causal Convolution by the Kernel'
tags: [research-papers, sequence-models, state-space, sequence]
difficulty: Advanced
---

## Statement

### The problem, from first principles

The S4 kernel turns the state space model into a causal convolution. Applying the kernel to the input is the same computation as running the recurrence, which the next question checks.

### From theory to code

Implement `causal_conv_from_kernel(K, x)`, the causal convolution of the input with the kernel.

### Constraints

- Entries of x before the start are zero.

### Hints

<details>
<summary>Hint 1</summary>

For each output step, sum the kernel taps times the inputs that many steps back, stopping at the start of the sequence.

</details>

## Theory

### The simple version

Convolution over the whole sequence can be done with FFTs, so the model trains in O(L log L) time instead of stepping through the recurrence.

### The formula

$$y_t = \sum_{k=0}^{t}K_k\,x_{t-k}$$

### How NumPy/PyTorch actually implements this

S4 implementations apply the kernel with an FFT-based convolution on the full sequence.

## Explanation

This is the discrete convolution with a causal kernel; the FFT version is what the paper uses for long sequences.
