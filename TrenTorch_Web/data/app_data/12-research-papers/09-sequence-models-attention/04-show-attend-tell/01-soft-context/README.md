---
name: research-sat-soft-context
title: 'Show, Attend and Tell: Soft Attention Context'
tags: [research-papers, sequence-models, attention, captioning]
difficulty: Beginner
---

## Statement

### The problem, from first principles

Show, Attend and Tell (Xu et al., 2015) captions images by attending to regions of a CNN feature map at each word. The context for a word is the attention-weighted average of the region features.

### From theory to code

Implement `soft_context(alpha, feats)`, the attention-weighted sum of the image features.

### Constraints

- Weights sum to one.

### Hints

<details>
<summary>Hint 1</summary>

Multiply the weight vector by the feature matrix.

</details>

## Theory

### The simple version

Soft attention is differentiable, so the model learns where to look by ordinary backpropagation rather than a sampling procedure.

### The formula

$$\hat z_t = \sum_{i=1}^{L}\alpha_{t,i}\,a_i$$

### How NumPy/PyTorch actually implements this

Image captioning models compute this context vector at each decoding step.

## Explanation

The paper's soft variant is this weighted average; the hard variant samples one location instead.
