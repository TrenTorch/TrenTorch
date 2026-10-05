---
name: lda-topic-conditional
title: 'LDA collapsed Gibbs topic conditional'
tags: [classical-ml, topic-models, lda, gibbs-sampling, dirichlet]
difficulty: Advanced
---

## Statement

### The topic distribution for one word, given all other assignments

Latent Dirichlet Allocation (Blei, Ng and Jordan, 2003) explains each document as a mixture of topics and each topic as a distribution over words. Collapsed Gibbs sampling (Griffiths and Steyvers, 2004) resamples the topic of one word token at a time. For that token, with its own assignment already removed from the counts, the conditional is

`p(z = k | rest) proportional to (n_dk + alpha) * (n_kw + beta) / (n_k + V beta)`.

Here `n_dk` counts the other tokens in the document assigned to topic `k`, `n_kw` counts occurrences of word `w` in topic `k`, `n_k` is the total count in topic `k`, and `V` is the vocabulary size.

Implement `topic_conditional(doc_counts, topic_word, topic_totals, alpha, beta, word)`.

- `doc_counts` is `(K,)`. `topic_word` is `(K, V)`. `topic_totals` is `(K,)`. `word` is an index in `0..V-1`.
- Return the normalized probability vector of length `K`.

### Constraints

- Shapes must be consistent. Otherwise raise `ValueError`.
- `alpha > 0` and `beta > 0`. Otherwise raise `ValueError`.
- Counts must be nonnegative. Otherwise raise `ValueError`.
- `word` must be in range. Otherwise raise `ValueError`.
- Do not modify the inputs.

### Hints

<details>
<summary>Hint 1</summary>

Multiply the three factors elementwise over topics, then divide by their sum. The denominator `n_k + V beta` is a vector over `k`, not a scalar.

</details>

## Theory

The collapsed sampler integrates out the topic proportions and the topic-word distributions, which leaves only counts. That makes each update a few array operations. The `alpha` term favours topics already present in the document, and the `beta` term favours topics that already use the word, so the sampler balances document-level and corpus-level structure. The conditional is the core of the whole algorithm: an error here shifts every downstream topic estimate.

### Where this shows up in production

Topic models are used for content routing and exploratory analysis of support tickets, research abstracts and product reviews. Gibbs samplers are the reference implementation behind many topic-modeling libraries, and their per-token conditional is what runs in the inner loop of large corpus jobs.

### Using it to make decisions

Use LDA when you need interpretable topics over a bag-of-words corpus and can tolerate that word order is ignored. Tune `alpha` and the number of topics on held-out perplexity or on a human-checked coherence score, not on training likelihood. For production routing, a fixed topic model is usually enough once fitted, so the sampler is a training tool rather than a serving component.

### Pros and cons

**Pros:** interpretable topics, a principled Bayesian treatment, and a simple conditional that is cheap to compute.

**Cons:** Gibbs sampling is slow to converge and sensitive to initialization, the number of topics must be chosen, and bag-of-words topics can be dominated by frequent, uninformative words unless the corpus is filtered.

## Explanation

The solution multiplies the document term, the word-given-topic term, and the inverse normalizer per topic, then normalizes. Using the count vector of the target word (a column of `topic_word`) keeps the computation vectorized across topics.
