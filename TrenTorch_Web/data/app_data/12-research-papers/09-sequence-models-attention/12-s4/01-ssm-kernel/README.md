---
name: research-s4-ssm-kernel
title: 'S4: The Convolution Kernel of an SSM'
tags: [research-papers, sequence-models, state-space, sequence]
difficulty: Advanced
---

## Statement

### The problem, from first principles

S4 (Gu et al., 2022) notices that a linear state space model is equivalent to a convolution. Unrolling the recurrence gives a kernel K whose k-th entry is C A^k B, and that kernel can be computed in parallel.

### From theory to code

Implement `ssm_kernel(A_bar, B_bar, C, L)`, the impulse response of the scalar system.

### Constraints

- Lags start at zero.

### Hints

<details>
<summary>Hint 1</summary>

Raise the state transition to each lag, multiply by C and B.

</details>

## Theory

### The simple version

Writing the model as a convolution lets training run in parallel over the sequence, while inference can still use the recurrence.

### The formula

$$K_k = C\,\bar A^{k}\,\bar B, \qquad k = 0,\ldots,L-1$$

### How NumPy/PyTorch actually implements this

S4 computes this kernel with a structured (diagonal plus low-rank) algorithm rather than explicit powers.

## Explanation

The kernel is the response to a single impulse, and the convolution of the input with it reproduces the recurrence.
