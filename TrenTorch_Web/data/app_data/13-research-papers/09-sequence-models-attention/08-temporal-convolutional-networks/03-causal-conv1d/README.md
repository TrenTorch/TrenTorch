---
name: research-tcn-causal-conv1d
title: 'TCN: A Causal 1D Convolution'
tags: [research-papers, sequence-models, convolution, sequence]
difficulty: Intermediate
---

## Statement

### The problem, from first principles

A causal 1D convolution computes each output from the current input and the few before it, never the future. It is the basic operation of a temporal convolutional network.

### From theory to code

Implement `causal_conv1d(x, w)`, the causal convolution with zeros before the start of the sequence.

### Constraints

- `w[0]` multiplies the current input.

### Hints

<details>
<summary>Hint 1</summary>

For each time step, sum the kernel taps times the inputs that many steps back, skipping positions before the start.

</details>

## Theory

### The simple version

Because each output depends only on past inputs, the model can generate sequences one step at a time without seeing the future.

### The formula

$$y_t = \sum_{j=0}^{k-1} w_j\, x_{t-j}, \qquad x_{s} = 0 \text{ for } s < 0$$

### How NumPy/PyTorch actually implements this

Deep learning frameworks implement this as `conv1d` on left-padded inputs.

## Explanation

The loop is a direct translation of the formula; the library version uses padded `conv1d` calls.
