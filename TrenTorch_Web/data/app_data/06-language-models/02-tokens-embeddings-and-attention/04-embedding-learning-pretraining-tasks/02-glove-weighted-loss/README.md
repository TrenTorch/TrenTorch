---
name: lm-glove-weighted-loss
title: GloVe & Co-occurrence Statistics
tags: [embeddings, glove, co-occurrence]
difficulty: Advanced
---

## Statement

### The problem, from first principles

Skip-gram learns from one pair at a time. **GloVe** first counts, over the whole corpus, how often each word `j` appears near each word `i`, giving a co-occurrence matrix `X`. It then fits vectors so that the dot product of two word vectors (plus biases) approximates the **logarithm** of their co-occurrence count. Two details make it work. Rare pairs have noisy counts and very frequent pairs ("the" with "of") would dominate, so each term is weighted by a function `f(x) = (x / x_max)^alpha`, capped at 1: small counts get small weight and large counts stop growing in importance. And pairs that never co-occur (`X = 0`) are skipped, because `log 0` is undefined.

### From theory to code

Implement `cooccurrence_matrix`, `glove_weight` and `glove_loss`.

### Constraints

- `cooccurrence_matrix(token_ids, V, window)` returns a `(V, V)` float array. For every position `i` and every `j` with `1 <= |i - j| <= window` inside the sequence, add `1 / |i - j|` to `X[token_ids[i], token_ids[j]]` (nearer words count more).
- `glove_weight(x, x_max, alpha)` is `(x / x_max) ** alpha` where `x < x_max`, else `1.0`, elementwise.
- `glove_loss(W, W_tilde, b, b_tilde, X, x_max, alpha)`: the sum over all `(i, j)` with `X[i, j] > 0` of `f(X[i, j]) * (W[i] @ W_tilde[j] + b[i] + b_tilde[j] - log X[i, j]) ** 2`. Return a float (sum, not mean).

### Hints

<details>
<summary>Hint 1</summary>

Use a boolean mask `X > 0` and the log only on masked entries, to avoid `log(0)` warnings.

</details>

<details>
<summary>Hint 2</summary>

`W @ W_tilde.T` gives all dot products at once.

</details>

## Theory

### The simple version

Instead of replaying every conversation, GloVe tallies a big table of who talks near whom, then finds coordinates for each word such that the distance-like score between two words matches the logarithm of how often they appeared together.

### The formula

$$
J = \sum_{i,j:\,X_{ij} > 0} f(X_{ij})\,\big(w_i^\top \tilde w_j + b_i + \tilde b_j - \ln X_{ij}\big)^2, \qquad f(x) = \min\!\big((x/x_{\max})^{\alpha}, 1\big)
$$

Pennington et al. used $x_{\max} = 100$ and $\alpha = 3/4$.

### How this is done in practice

Pre-trained GloVe vectors (trained on Common Crawl and Wikipedia) are a standard baseline for text classifiers. The final embedding is usually `W + W_tilde`. Matrix-factorization views of word2vec show the two methods are closely related.

## Explanation

Counting, a weight function and a masked weighted least-squares loss. The test with a perfectly fitted model, whose loss is exactly zero, confirms the log-count target and the mask.
