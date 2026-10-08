---
name: research-gru-step
title: 'Learning Phrase Representations: One Full GRU Step'
tags: [research-papers, transformers, llm, recurrent, gru]
difficulty: Advanced
---

## Statement

### The problem, from first principles

Putting the pieces together gives one full GRU step. The update gate decides how much of the candidate to take, and the candidate already uses the reset gate. The output blends the old state and the candidate.

### From theory to code

Implement `gru_step(x, h, Wz, Uz, Wr, Ur, W, U)`, computing the update gate, the reset gate, the candidate, and the new state.

### Constraints

- All weight matrices have the shapes shown in the docstring.

### Hints

<details>
<summary>Hint 1</summary>

Compute `z`, `r`, `h_tilde`, then return `(1 - z) * h + z * h_tilde`.

</details>

## Theory

### The simple version

The update gate interpolates between the old state and the candidate. A closed gate copies the previous state, which is how a GRU carries information across many steps.

### The formula

$$h_t = (1 - z_t) \odot h_{t-1} + z_t \odot \tilde h_t$$

### How NumPy/PyTorch actually implements this

`torch.nn.GRUCell` returns this state; a `torch.nn.GRU` runs the same step over a whole sequence.

## Explanation

This is the complete recurrence from the paper. Stacking steps over a sequence gives the encoder and decoder of RNN-based translation.
