---
name: lda-topic-estimates
title: 'LDA point estimates for topic mixtures and word distributions'
tags: [classical-ml, topic-models, lda, smoothing, dirichlet]
difficulty: Intermediate
---

## Statement

### Turn Gibbs counts into document and topic distributions

After Gibbs sampling, the count matrices hold the final topic assignments. The usual point estimates add the Dirichlet priors back in:

- Document-topic mixture: `theta[d, k] = (n_dk + alpha) / (sum_k' n_dk' + K alpha)`.
- Topic-word distribution: `phi[k, w] = (n_kw + beta) / (sum_w' n_kw' + V beta)`.

Implement `lda_estimates(doc_topic, topic_word, alpha, beta)`, which returns `(theta, phi)`.

- `doc_topic` is `(D, K)` with nonnegative counts. `topic_word` is `(K, V)` with nonnegative counts.
- `theta` has shape `(D, K)`, and `phi` has shape `(K, V)`. Each row of both sums to 1.

### Constraints

- Shapes must be consistent (`doc_topic` has `K` columns and `topic_word` has `K` rows). Otherwise raise `ValueError`.
- `alpha > 0` and `beta > 0`. Otherwise raise `ValueError`.
- Counts must be nonnegative. Otherwise raise `ValueError`.
- Do not modify the inputs.

### Hints

<details>
<summary>Hint 1</summary>

Add the prior to every cell, then divide by the row sum of the smoothed counts. Equivalently, the denominator is `row_total + K alpha` for theta and `row_total + V beta` for phi.

</details>

## Theory

These estimates are posterior means under the Dirichlet priors, so they never assign zero probability to an unseen topic-word pair. That smoothing matters both for interpretability and for scoring held-out documents, where a zero would make a whole document impossible. The prior strength controls sparsity: small `alpha` gives documents dominated by a few topics, and small `beta` gives topics dominated by a few words.

### Where this shows up in production

The `theta` vectors are what products consume: a document's topic mix becomes a feature for routing, clustering, or recommendation. The `phi` matrix supplies top words per topic for dashboards and for human review of topic quality.

### Using it to make decisions

Use `theta` as a compact document representation when you need interpretable features with a few dimensions. Check the topics with their top words before using them, since a topic of stop words is a sign that the corpus needs better filtering. Tune `alpha` and `beta` using held-out perplexity or topic coherence, and keep the same priors in training and serving so the mixtures stay comparable.

### Pros and cons

**Pros:** smooth, interpretable, and nonzero everywhere, which keeps downstream scoring stable.

**Cons:** the smoothing shifts small counts a lot, the number of topics is still a manual choice, and topics can be unstable across random seeds, so they need a stability check before they are used as a feature.

## Explanation

The solution adds the prior to every count and divides by the smoothed row total. Because the smoothed row sums to the same constant in every row, each output row is a valid probability distribution.
