---
name: research-mamba-selective-step
title: 'Mamba: The Selective Step Size'
tags: [research-papers, sequence-models, state-space, sequence]
difficulty: Intermediate
---

## Statement

### The problem, from first principles

Mamba's step size depends on the current input, through a softplus so it stays positive. A large step lets the state absorb the current token, and a small step lets it ignore it. That input-dependent choice is the selection mechanism.

### From theory to code

Implement `selective_step(delta_raw)`, mapping a raw value to a positive step size.

### Constraints

- Use a stable softplus.

### Hints

<details>
<summary>Hint 1</summary>

Compute the log of one plus the exponential of the raw value, using logaddexp for stability.

</details>

## Theory

### The simple version

Softplus keeps the step positive and smooth. The model decides per token how much of the past to keep, which is the selectivity that distinguishes Mamba from fixed linear systems.

### The formula

$$\Delta_t = \operatorname{softplus}\big(W_\Delta x_t + b_\Delta\big)$$

### How NumPy/PyTorch actually implements this

Mamba's selective scan takes delta from a linear projection of each input token.

## Explanation

The softplus is the same function as in Deep InfoMax, here used to bound the discretization step.
