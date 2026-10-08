---
name: research-rope-frequencies
title: 'RoFormer: The Rotary Frequencies'
tags: [research-papers, transformers, llm, position, rope]
difficulty: Intermediate
---

## Statement

### The problem, from first principles

RoFormer (Su et al., 2021) encodes position by rotating query and key vectors, rather than adding a position vector. Each pair of features rotates at its own frequency, so the dot product between a rotated query and key depends on how far apart their positions are.

### From theory to code

Implement `rope_frequencies(d, base)`, returning the `d / 2` rotation frequencies.

### Constraints

- `d` is even.

### Hints

<details>
<summary>Hint 1</summary>

Compute `base ** (-2 i / d)` for `i` in `0 .. d/2 - 1` as one vector.

</details>

## Theory

### The simple version

The first pair rotates fastest and later pairs slowly, like the sinusoidal encoding's frequency spread, but applied as rotations inside attention.

### The formula

$$\theta_i = \text{base}^{-2i/d}, \qquad i = 0, \ldots, \tfrac{d}{2} - 1$$

### How NumPy/PyTorch actually implements this

Llama-style code precomputes the same frequency vector for `freqs_cis` in the rotary embedding module.

## Explanation

A single vector of frequencies is shared by every position, so it is computed once per model dimension.
