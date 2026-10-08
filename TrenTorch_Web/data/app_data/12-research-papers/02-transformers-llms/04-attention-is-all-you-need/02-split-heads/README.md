---
name: research-multihead-split
title: 'Attention Is All You Need: Splitting Into Heads'
tags: [research-papers, transformers, llm, attention, transformer]
difficulty: Beginner
---

## Statement

### The problem, from first principles

Multi-head attention runs several attention functions in parallel, each on a smaller slice of the features. Splitting the vectors into heads is the first step, and it costs no extra parameters.

### From theory to code

Implement `split_heads(x, h)`, which turns a `(T, d)` sequence into `(h, T, d // h)`.

### Constraints

- `d` must be divisible by `h`.

### Hints

<details>
<summary>Hint 1</summary>

Reshape to `(T, h, d // h)`, then transpose so the head axis comes first.

</details>

## Theory

### The simple version

Each head gets `d / h` features per position. Because the slices don't overlap, the heads learn different relationships.

### The formula

$$x \in \mathbb{R}^{T \times d} \;\longrightarrow\; \mathbb{R}^{h \times T \times d/h}$$

### How NumPy/PyTorch actually implements this

`x.view(T, h, d // h).transpose(0, 1)` in PyTorch performs the same split.

## Explanation

The reshape and transpose are views, not copies, in NumPy and PyTorch, so splitting is essentially free.
