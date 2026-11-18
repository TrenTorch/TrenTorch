---
name: research-w2v-skipgram-prob
title: 'word2vec: The Skip-gram Softmax'
tags: [research-papers, unsupervised, word-embeddings, word2vec]
difficulty: Intermediate
---

## Statement

### The problem, from first principles

Skip-gram models the probability that a context word appears near a center word. A full softmax over the vocabulary gives the probability, using the dot products between the center vector and every output vector.

### From theory to code

Implement `skipgram_probability(v_c, U, o)`, returning the softmax probability of the observed context word.

### Constraints

- Subtract the maximum score before exponentiating.

### Hints

<details>
<summary>Hint 1</summary>

Compute `U @ v_c`, apply a stable softmax, then read the entry at `o`.

</details>

## Theory

### The simple version

Words that share contexts get similar vectors, so their dot products are large and the model assigns them high probability. The embedding geometry therefore encodes co-occurrence.

### The formula

$$P(w_o \mid w_c) = \frac{\exp(u_o^\top v_c)}{\sum_{w=1}^{V}\exp(u_w^\top v_c)}$$

### How NumPy/PyTorch actually implements this

`torch.nn.functional.log_softmax(U @ v_c)` computes the same log-probability.

## Explanation

The full softmax is expensive for large vocabularies, which motivates the negative sampling question in the next paper.
