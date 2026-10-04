---
name: lm-additive-attention
title: Additive Attention
tags: [attention, seq2seq, alignment]
difficulty: Intermediate
---

## Statement

### The problem, from first principles

Before the transformer, attention was invented to fix a bottleneck in translation: an encoder squeezed a whole sentence into one vector. Bahdanau's idea was to keep all encoder states and let the decoder _look back_ at them with a learned relevance score. The score between a decoder query `q` and each encoder state `k_t` comes from a tiny one-hidden-layer network: `v^T tanh(W_q q + W_k k_t)`. A softmax over the scores gives attention weights and the **context vector** is the weighted average of the encoder states. The transformer replaced this additive score with a cheaper dot product, but the weighted-average idea is identical.

### From theory to code

Implement `additive_attention`.

### Constraints

- `query` has shape `(d_q,)`, `keys` has shape `(T, d_k)`. `W_q` is `(d_q, h)`, `W_k` is `(d_k, h)` and `v` is `(h,)`.
- Scores are `tanh(query @ W_q + keys @ W_k) @ v`, shape `(T,)`. Weights are a numerically stable softmax over the scores.
- The context vector is `weights @ keys`, shape `(d_k,)`. Return `(context, weights)`.

### Hints

<details>
<summary>Hint 1</summary>

`query @ W_q` has shape `(h,)` and broadcasts against `keys @ W_k` of shape `(T, h)`.

</details>

<details>
<summary>Hint 2</summary>

Subtract the maximum score before exponentiating.

</details>

## Theory

### The simple version

When translating a sentence you glance back at the source words most relevant to the word you are about to write. The score network is the part of your brain that decides which source word to glance at.

### The formula

$$
e_t = v^\top \tanh(W_q q + W_k k_t), \qquad
\alpha_t = \frac{e^{e_t}}{\sum_s e^{e_s}}, \qquad
c = \sum_t \alpha_t k_t
$$

Compare with scaled dot-product attention, $e_t = q^\top k_t / \sqrt d$: additive attention has parameters and a hidden layer, dot-product has none and runs as one matrix multiplication.

### How this is done in practice

`torch.nn.MultiheadAttention` implements the dot-product form because it maps onto fast matrix multiplication, while additive attention survives in some pointer networks and keyword-spotting models. Bahdanau's decoder used it with a bidirectional recurrent encoder.

## Explanation

One hidden layer scores every key against the query, a softmax normalizes and a weighted sum returns the context. The weights are returned because attention maps are how translation models were originally inspected: the weight matrix shows word alignment.
