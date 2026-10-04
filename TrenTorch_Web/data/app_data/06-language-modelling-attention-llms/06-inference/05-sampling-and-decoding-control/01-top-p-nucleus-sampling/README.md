---
name: lm-top-p-nucleus-sampling
title: Top-p Sampling
tags: [decoding, sampling, top-p]
difficulty: Intermediate
---

## Statement

### The problem, from first principles

Sampling from the full distribution occasionally picks a token from the long tail of unlikely, incoherent options, and top-k sampling uses a fixed number of candidates whether the model is certain or unsure. **Nucleus (top-p) sampling** adapts: sort tokens by probability and keep the smallest set whose cumulative probability reaches `p`. When the model is confident the nucleus is a token or two, when it is unsure the nucleus is wide. The kept probabilities are renormalized so they sum to one and sampling proceeds from this truncated distribution.

### From theory to code

Implement `top_p_filter`.

### Constraints

- `probs` is a 1-D probability vector and `0 < p <= 1`. Sort descending (stable, ties by lower index first).
- Keep the smallest prefix of the sorted order whose cumulative probability is `>= p`. At least one token is always kept.
- Return a vector of the same length with the kept tokens renormalized to sum to 1 and every other entry exactly `0`.
- Do not modify `probs`.

### Hints

<details>
<summary>Hint 1</summary>

`np.argsort(-probs, kind='stable')` gives a stable descending order.

</details>

<details>
<summary>Hint 2</summary>

The first index where the cumulative sum reaches `p` (use `np.searchsorted(cum, p - 1e-12)` or compare with a small tolerance) marks the end of the nucleus.

</details>

## Theory

### The simple version

Imagine ranking guests by how likely they are to be the one who knocked. You stop adding names once the list covers 90% of the chance, and ignore the rest.

### The formula

$$
V_p = \text{smallest set such that } \sum_{i \in V_p} p_i \ge p, \qquad
\tilde p_i = \frac{p_i\,\mathbf{1}[i \in V_p]}{\sum_{j \in V_p} p_j}
$$

### How this is done in practice

Hugging Face's `TopPLogitsWarper` and every serving stack implement this. It is usually applied after temperature scaling and often together with top-k, and the order of the filters changes the result.

## Explanation

Sorting, a cumulative sum and one comparison locate the cut. Because at least one token is always kept, `p` close to 0 degenerates cleanly to greedy decoding.
