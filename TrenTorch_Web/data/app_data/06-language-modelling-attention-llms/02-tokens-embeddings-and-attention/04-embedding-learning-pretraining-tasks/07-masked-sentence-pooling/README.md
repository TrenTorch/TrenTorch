---
name: lm-masked-sentence-pooling
title: Sentence Pooling
tags: [pretraining, sentence-embeddings, pooling]
difficulty: Intermediate
---

## Statement

### The problem, from first principles

A transformer outputs one vector per token, but classification and retrieval need **one vector per sentence**. Three standard ways to pool: take the vector of the special first token (`[CLS]`), which the model was trained to summarize the input; take the **mean** over the tokens; or take the elementwise **max**. In a batch, sequences are padded, and padding positions hold meaningless vectors, so mean and max must use only the **real** tokens as marked by the attention mask. A mean that includes padding is silently biased toward zero and changes with how much padding the batch happens to have.

### From theory to code

Implement `pool_sentence`.

### Constraints

- `hidden` has shape `(B, T, d)` and `mask` has shape `(B, T)` with 1 for real tokens and 0 for padding. Every row has at least one real token, and real tokens come first (right padding).
- `pool_sentence(hidden, mask, mode)` returns `(B, d)`. `'cls'`: `hidden[:, 0]`. `'mean'`: the average over positions where `mask == 1`. `'max'`: the elementwise maximum over positions where `mask == 1`. Any other mode raises `ValueError`.

### Hints

<details>
<summary>Hint 1</summary>

Mean: `(hidden * mask[..., None]).sum(1) / mask.sum(1, keepdims=True)`.

</details>

<details>
<summary>Hint 2</summary>

Max: set padded positions to `-inf` before taking the maximum.

</details>

## Theory

### The simple version

Summarizing a group photo with a few people cut out: the average expression is taken over the people in the picture, not over the blank spots where the cut-outs were.

### The formula

$$
s_{\text{mean}} = \frac{\sum_t m_t h_t}{\sum_t m_t}, \qquad s_{\text{max}} = \max_{t:\,m_t = 1} h_t, \qquad s_{\text{cls}} = h_0
$$

### How this is done in practice

Sentence-BERT uses mean pooling over the token states for its sentence embeddings, and BERT classifiers use the `[CLS]` state. Decoder-only embedding models usually take the last real token instead, which is why the padding side matters.

## Explanation

The implementation is a masked reduction. The padding-invariance test is the real check: changing the contents of padded positions must not change the result.
