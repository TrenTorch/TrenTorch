---
name: research-ns-unigram-noise
title: 'Negative Sampling: The Noise Distribution'
tags: [research-papers, unsupervised, word-embeddings, negative-sampling]
difficulty: Intermediate
---

## Statement

### The problem, from first principles

Negatives should be random words, but not only the most common ones, which would be trivial to reject. Word2vec draws negatives from the unigram distribution raised to the power 3/4, a compromise that gives rare words more chances than their raw frequency.

### From theory to code

Implement `unigram_noise(counts, power)`, returning the normalized counts raised to `power`.

### Constraints

- The default power is 0.75.

### Hints

<details>
<summary>Hint 1</summary>

Raise the counts to `power`, then divide by the sum.

</details>

## Theory

### The simple version

Power 3/4 boosts rare words relative to plain frequency, so the model sees more varied negatives and learns better vectors for them.

### The formula

$$P_n(w) = \frac{f(w)^{3/4}}{\sum_{w'} f(w')^{3/4}}$$

### How NumPy/PyTorch actually implements this

Word2vec samplers precompute a table from these probabilities to draw negatives quickly.

## Explanation

A power below one flattens the distribution. The exponent is a tuned choice from the paper, not a theorem.
