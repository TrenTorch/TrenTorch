---
name: research-gru-update-gate
title: 'Learning Phrase Representations: The GRU Update Gate'
tags: [research-papers, transformers, llm, recurrent, gru]
difficulty: Beginner
---

## Statement

### The problem, from first principles

A gated recurrent unit decides how much of its old state to keep and how much to replace. The update gate is the first decision: it is a vector of values between 0 and 1 computed from the current input and the previous state.

### From theory to code

Implement `gru_update_gate(x, h, Wz, Uz)`, which returns `sigmoid(Wz x + Uz h)`.

### Constraints

- Output values are strictly between 0 and 1.

### Hints

<details>
<summary>Hint 1</summary>

Compute the affine map of `x` and `h`, then apply the logistic function element-wise.

</details>

## Theory

### The simple version

A gate near 1 means the new candidate state replaces the old one; near 0 means the old state is kept. The gate is learned per dimension.

### The formula

$$z_t = \sigma(W_z x_t + U_z h_{t-1})$$

### How NumPy/PyTorch actually implements this

`torch.nn.GRUCell` computes this gate internally as part of its update.

## Explanation

The sigmoid is written with `np.exp`, matching the logistic function in the paper.
