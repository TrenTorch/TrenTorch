---
name: research-las-pyramid-length
title: 'Listen, Attend and Spell: Pyramidal Length'
tags: [research-papers, sequence-models, speech, attention]
difficulty: Beginner
---

## Statement

### The problem, from first principles

Listen, Attend and Spell (Chan et al., 2016) reads thousands of speech frames. A pyramidal encoder halves the time resolution at each layer, so the attention decoder works over a much shorter sequence.

### From theory to code

Implement `pyramid_length(T, layers)`, the length after the pyramidal reduction.

### Constraints

- Round up at each halving.

### Hints

<details>
<summary>Hint 1</summary>

Divide the length by two to the power of the layer count, rounding up.

</details>

## Theory

### The simple version

Shorter encoder sequences make attention over speech feasible, since the cost of attention grows with the square of the length.

### The formula

$$T' = \left\lceil\frac{T}{2^{L}}\right\rceil$$

### How NumPy/PyTorch actually implements this

Speech recognizers implement this pyramid by stacking frame-concatenating bidirectional LSTM layers.

## Explanation

Each pyramidal layer concatenates adjacent frames, which halves the length and doubles the features.
