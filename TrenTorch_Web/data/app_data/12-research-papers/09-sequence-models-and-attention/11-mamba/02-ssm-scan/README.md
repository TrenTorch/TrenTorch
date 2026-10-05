---
name: research-mamba-ssm-scan
title: 'Mamba: The Recurrent Scan'
tags: [research-papers, sequence-models, state-space, sequence]
difficulty: Advanced
---

## Statement

### The problem, from first principles

Once discretized, the state space model is a linear recurrence over the input. Mamba computes this scan efficiently, and the parameters vary per token, which is what makes it selective.

### From theory to code

Implement `ssm_scan(a, b, x)`, the recurrence over an input sequence.

### Constraints

- The initial state is zero.

### Hints

<details>
<summary>Hint 1</summary>

Start the state at zero, then for each input update it as a times the state plus b times the input.

</details>

## Theory

### The simple version

A linear recurrence can be computed with a parallel scan during training and as a cheap recurrence at inference, combining the strengths of RNNs and transformers.

### The formula

$$h_t = \bar A\,h_{t-1} + \bar B\,x_t, \qquad y_t = C\,h_t$$

### How NumPy/PyTorch actually implements this

Mamba's CUDA kernel performs this scan in parallel over the sequence length.

## Explanation

The scalar version here is the core of the scan; Mamba uses a hardware-aware parallel implementation of the same recurrence.
