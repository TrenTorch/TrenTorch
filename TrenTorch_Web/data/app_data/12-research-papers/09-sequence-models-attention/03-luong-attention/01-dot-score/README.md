---
name: research-luong-dot-score
title: 'Luong Attention: The Dot Score'
tags: [research-papers, sequence-models, attention, translation]
difficulty: Beginner
---

## Statement

### The problem, from first principles

Luong et al. (2015) score decoder-encoder alignments in three ways. The simplest is the dot product: states that point the same way get high scores, with no extra parameters.

### From theory to code

Implement `dot_score(h_t, h_s)`, the dot product of the decoder and encoder states.

### Constraints

- Returns a float.

### Hints

<details>
<summary>Hint 1</summary>

Compute the dot product of the two vectors.

</details>

## Theory

### The simple version

Dot scores are the cheapest alignment, and they work well when the decoder and encoder share a representation space.

### The formula

$$\text{score}(h_t, \bar h_s) = h_t^\top \bar h_s$$

### How NumPy/PyTorch actually implements this

Transformer attention is a scaled dot product of the same form.

## Explanation

Without a learned matrix the score depends only on the geometry of the two states.
