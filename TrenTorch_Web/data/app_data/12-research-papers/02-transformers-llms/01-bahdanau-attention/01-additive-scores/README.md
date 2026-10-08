---
name: research-bahdanau-additive-scores
title: 'Bahdanau Attention: Additive Alignment Scores'
tags: [research-papers, transformers, llm, attention]
difficulty: Intermediate
---

## Statement

### The problem, from first principles

Bahdanau et al. (2014) let a decoder look back at every encoder state when producing each output word. The alignment score measures how relevant each encoder state is to the decoder's current state, using a small learned network.

### From theory to code

Implement `additive_scores(s, H, W, U, v)`, which returns one score per encoder state: `v . tanh(W s + U h_j)`.

### Constraints

- `H` has shape `(T, d_h)`.

### Hints

<details>
<summary>Hint 1</summary>

Broadcast the decoder state against every encoder row, apply `tanh`, then dot with `v`.

</details>

## Theory

### The simple version

The score asks: is this encoder position relevant to what the decoder needs now? The learned `W`, `U` and `v` define that relevance, so the network decides what to attend to.

### The formula

$$e_j = v^\top \tanh(W s + U h_j)$$

### How NumPy/PyTorch actually implements this

PyTorch implements this in attention modules such as `torch.nn.MultiheadAttention`'s predecessors; the additive form is written out in many seq2seq tutorials.

## Explanation

`s @ W.T` is a single vector, `H @ U.T` is one row per encoder state, and their sum broadcasts across the rows before `tanh`.
