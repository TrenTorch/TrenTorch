---
name: research-luong-local-window
title: 'Luong Attention: The Local Window'
tags: [research-papers, sequence-models, attention, translation]
difficulty: Beginner
---

## Statement

### The problem, from first principles

Local attention (Luong et al., 2015) looks only at a window of source positions around a predicted alignment point. It is cheaper than attending to the whole sentence, and the window keeps the search focused.

### From theory to code

Implement `local_window(center, D, T)`, returning the window of source positions to attend to.

### Constraints

- Clip the window to the valid range 0 to T.

### Hints

<details>
<summary>Hint 1</summary>

Take the window from center minus D to center plus D inclusive, then clamp both ends to the sentence.

</details>

## Theory

### The simple version

The window limits the attention cost per decoder step to a constant, independent of the sentence length.

### The formula

$$[p_t - D,\; p_t + D] \cap [0, T)$$

### How NumPy/PyTorch actually implements this

Local attention variants in translation toolkits compute the same clipped slice of the encoder states.

## Explanation

The predicted position p_t is learned; the window only restricts where the softmax is evaluated.
