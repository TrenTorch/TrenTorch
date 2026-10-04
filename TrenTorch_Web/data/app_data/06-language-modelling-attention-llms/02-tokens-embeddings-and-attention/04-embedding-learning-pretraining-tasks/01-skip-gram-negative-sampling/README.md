---
name: lm-skip-gram-negative-sampling
title: Skip-Gram with Negative Sampling
tags: [embeddings, word2vec, negative-sampling]
difficulty: Intermediate
---

## Statement

### The problem, from first principles

Word embeddings are learned from a simple game: given a word, predict the words around it. In the **skip-gram** model each word has two vectors, one used when it is the _center_ and one when it appears as _context_. Scoring every possible context word with a softmax over the whole vocabulary is far too expensive, so **negative sampling** turns the problem into binary classification: the true (center, context) pair should score high, and a handful of randomly drawn _negative_ words should score low. The score of a pair is the dot product of the two vectors, passed through a sigmoid. Training pulls vectors of words that share contexts together, which is why similar words end up with similar vectors.

### From theory to code

Implement `skipgram_pairs` and `sgns_loss`.

### Constraints

- `skipgram_pairs(token_ids, window)` returns a list of `(center, context)` pairs. For each position `i` in order, the contexts are the tokens at positions `i - window .. i + window` (inside the sequence, excluding `i`), in increasing position order.
- `W_in` and `W_out` are `(V, d)` arrays: `W_in[c]` is the center vector and `W_out[o]` the context vector. `sgns_loss(W_in, W_out, center, context, negatives)` takes integer arrays `center` and `context` of shape `(B,)` and `negatives` of shape `(B, K)`.
- For each example the loss is `-log sigmoid(u_o . v_c) - sum_k log sigmoid(-u_k . v_c)`. Return the **mean over examples** as a float. Use `np.logaddexp(0, -x)` for `-log sigmoid(x)`.

### Hints

<details>
<summary>Hint 1</summary>

Gather the vectors with fancy indexing, then use `einsum` or `(a * b).sum(-1)` for the dot products.

</details>

<details>
<summary>Hint 2</summary>

`-log sigmoid(-x) = logaddexp(0, x)`.

</details>

## Theory

### The simple version

Think of a party game: you are told a word and must pick which of several words tends to show up near it. Real neighbours should win and random words from the dictionary should lose.

### The formula

$$
\mathcal{L} = -\ln\sigma(u_o^\top v_c) - \sum_{k=1}^{K}\ln\sigma(-u_k^\top v_c)
$$

With all vectors zero every sigmoid is $1/2$, so the loss is $(1 + K)\ln 2$.

### How this is done in practice

Word2vec's original implementation draws negatives from the unigram distribution raised to the power 3/4, and frequent words are subsampled. Gensim implements the same objective, and the idea of contrastive scoring against sampled negatives later reappears in CLIP and in two-tower retrieval models.

## Explanation

Pair generation is two nested loops over positions. The loss is a batched dot product followed by two stable log-sigmoid terms. The zero-vector test pins the constant `(1 + K) ln 2`, which is the loss of a model that knows nothing.
