---
name: research-ns-subsample
title: 'Negative Sampling: Subsampling Frequent Words'
tags: [research-papers, unsupervised, word-embeddings, negative-sampling]
difficulty: Beginner
---

## Statement

### The problem, from first principles

The most frequent words, such as 'the', carry little information and dominate the training pairs. Word2vec discards some of their occurrences at random, which speeds up training and improves the quality of the rarer words.

### From theory to code

Implement `subsample_keep_prob(freq, t)`, returning the probability of keeping an occurrence, capped at 1.

### Constraints

- The threshold `t` is usually around 1e-5 to 1e-4.

### Hints

<details>
<summary>Hint 1</summary>

Compute `sqrt(t / freq)` and take the minimum with 1.

</details>

## Theory

### The simple version

A word more frequent than the threshold is kept with a probability that falls with its frequency. Rare words, below the threshold, are always kept.

### The formula

$$P(\text{keep } w) = \min\left(1, \sqrt{\frac{t}{f(w)}}\right)$$

### How NumPy/PyTorch actually implements this

Word2vec implementations such as Gensim apply the same keep probability per token during training.

## Explanation

The formula is the subsampling rule from the paper. It keeps the training signal for rare words while cutting the redundant frequent ones.
