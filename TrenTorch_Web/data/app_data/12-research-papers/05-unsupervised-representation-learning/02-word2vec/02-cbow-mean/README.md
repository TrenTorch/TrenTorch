---
name: research-w2v-cbow-mean
title: 'word2vec: The CBOW Context Average'
tags: [research-papers, unsupervised, word-embeddings, word2vec]
difficulty: Beginner
---

## Statement

### The problem, from first principles

CBOW predicts a center word from its surrounding context. The context words' embeddings are averaged into one vector, so the model does not depend on the order of the context.

### From theory to code

Implement `cbow_context_mean(context_vectors)`, returning the average of the context embeddings.

### Constraints

- The result has the embedding dimension.

### Hints

<details>
<summary>Hint 1</summary>

Average the rows of the matrix.

</details>

## Theory

### The simple version

Averaging makes CBOW cheap and order-insensitive. It trades away word order information, which skip-gram keeps by predicting each neighbour separately.

### The formula

$$\bar v = \frac{1}{c}\sum_{j \in \text{context}} v_{w_j}$$

### How NumPy/PyTorch actually implements this

Gensim's CBOW mode performs this mean internally during training.

## Explanation

The averaged vector feeds a softmax over the vocabulary, the same output layer skip-gram uses.
