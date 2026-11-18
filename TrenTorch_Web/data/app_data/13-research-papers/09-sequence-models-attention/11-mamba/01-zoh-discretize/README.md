---
name: research-mamba-zoh-discretize
title: 'Mamba: Discretizing the State Space'
tags: [research-papers, sequence-models, state-space, sequence]
difficulty: Advanced
---

## Statement

### The problem, from first principles

Mamba (Gu & Dao, 2023) models sequences with a continuous linear system, then discretizes it with a step size that the input controls. Zero-order hold gives the discrete state transition and input gain.

### From theory to code

Implement `zoh_discretize(A, B, delta)`, the discrete transition and input for one step.

### Constraints

- Scalar state for this exercise.

### Hints

<details>
<summary>Hint 1</summary>

A_bar is the exponential of delta times A; B_bar is (A_bar minus one) divided by A, times B.

</details>

## Theory

### The simple version

The step size delta sets how much the state forgets per token. Mamba makes delta depend on the input, which is what makes the model selective.

### The formula

$$\bar A = e^{\Delta A}, \qquad \bar B = (\Delta A)^{-1}(\bar A - I)\,\Delta B$$

### How NumPy/PyTorch actually implements this

Mamba's implementation computes these discrete parameters per token before its parallel scan.

## Explanation

The scalar case simplifies the matrix formula to the division shown; the paper's form reduces to it for one state.
