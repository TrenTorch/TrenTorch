---
name: research-sinusoidal-positional-encoding
title: 'Attention Is All You Need: Sinusoidal Positions'
tags: [research-papers, transformers, llm, attention, transformer]
difficulty: Intermediate
---

## Statement

### The problem, from first principles

A transformer has no recurrence, so it needs another way to know word order. The paper adds fixed sine and cosine waves of different frequencies to the embeddings. Each position gets a unique pattern, and the model can learn to attend by relative offset.

### From theory to code

Implement `sinusoidal_positional_encoding(T, d)`, which returns the `(T, d)` table of sines and cosines.

### Constraints

- `d` is even.

### Hints

<details>
<summary>Hint 1</summary>

Build the angle matrix `pos / 10000^(2i/d)`, then fill even columns with `sin` and odd columns with `cos`.

</details>

## Theory

### The simple version

Low dimensions vary quickly with position and high dimensions slowly, so the combined pattern identifies each position uniquely.

### The formula

$$PE_{(pos, 2i)} = \sin\!\left(\frac{pos}{10000^{2i/d}}\right), \qquad PE_{(pos, 2i+1)} = \cos\!\left(\frac{pos}{10000^{2i/d}}\right)$$

### How NumPy/PyTorch actually implements this

Many implementations build this table once with NumPy broadcasting, the same `arange` and outer-product trick used here.

## Explanation

The table is computed once and added to the token embeddings. Because it is deterministic, it extends to any sequence length.
