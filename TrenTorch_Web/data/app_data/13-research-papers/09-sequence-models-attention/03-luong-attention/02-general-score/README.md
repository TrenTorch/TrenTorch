---
name: research-luong-general-score
title: 'Luong Attention: The General Score'
tags: [research-papers, sequence-models, attention, translation]
difficulty: Intermediate
---

## Statement

### The problem, from first principles

The general score adds a learned matrix between the two states. It lets the decoder and encoder live in different spaces and still be compared.

### From theory to code

Implement `general_score(h_t, W, h_s)`, the bilinear alignment score.

### Constraints

- Returns a float.

### Hints

<details>
<summary>Hint 1</summary>

Multiply the decoder state by the matrix, then dot with the encoder state.

</details>

## Theory

### The simple version

The learned matrix costs parameters, but it generalizes the dot score: the identity recovers it exactly.

### The formula

$$\text{score}(h_t, \bar h_s) = h_t^\top W_a \bar h_s$$

### How NumPy/PyTorch actually implements this

Luong-style attention layers implement this with one `Linear` on the encoder states before the dot product.

## Explanation

The bilinear form is the same shape as the discriminator score in Deep InfoMax, applied to translation states.
