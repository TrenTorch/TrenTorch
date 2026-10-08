---
name: research-w2v-skipgram-pairs
title: 'word2vec: Building Skip-gram Pairs'
tags: [research-papers, unsupervised, word-embeddings, word2vec]
difficulty: Beginner
---

## Statement

### The problem, from first principles

Word2vec (Mikolov et al., 2013) learns word vectors by predicting context words from a center word. Each word and each neighbour within a fixed window forms one training pair.

### From theory to code

Implement `skipgram_pairs(tokens, window)`, returning every (center, context) pair within the window.

### Constraints

- A word is not paired with itself.

### Hints

<details>
<summary>Hint 1</summary>

For each position, loop over the neighbours inside the window and skip the center.

</details>

## Theory

### The simple version

Pairs from nearby words teach the model which words appear together. The window size controls whether the vectors capture syntax (small windows) or topic (large windows).

### The formula

$$\mathcal{D} = \{(w_t, w_{t+j}) : 1 \le |j| \le c\}$$

### How NumPy/PyTorch actually implements this

Gensim's `Word2Vec` builds these windows internally before training.

## Explanation

The pairs are generated once per corpus pass and then sampled in mini-batches.
