---
name: research-gru-candidate
title: 'Learning Phrase Representations: The Candidate State'
tags: [research-papers, transformers, llm, recurrent, gru]
difficulty: Intermediate
---

## Statement

### The problem, from first principles

The candidate is what the unit would move to if it were fully updated. The reset gate lets the unit ignore the old state when computing that candidate, so it can start a fresh representation after an irrelevant part of the input.

### From theory to code

Implement `gru_candidate(x, h, r, W, U)`, which returns `tanh(W x + U (r * h))`.

### Constraints

- The reset gate multiplies `h` element-wise before the recurrent product.

### Hints

<details>
<summary>Hint 1</summary>

Compute `r * h` first, apply `U` to it, add `W x`, then `tanh`.

</details>

## Theory

### The simple version

When the reset gate is 0 the previous state has no influence, so the candidate depends only on the current input.

### The formula

$$\tilde h_t = \tanh(W x_t + U(r_t \odot h_{t-1}))$$

### How NumPy/PyTorch actually implements this

`torch.nn.GRUCell` computes this candidate with its own weights as one step of the cell.

## Explanation

The element-wise product `r * h` is the reset; the rest is a standard recurrent layer with a tanh nonlinearity.
