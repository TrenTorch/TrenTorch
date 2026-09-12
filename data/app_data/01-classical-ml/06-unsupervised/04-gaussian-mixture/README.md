---
name: unsupervised-gaussian-mixture
title: Gaussian Mixture Clustering
tags: [classical-ml, unsupervised, clustering, gaussian-mixture]
difficulty: Advanced
---

## Statement

Implement:

```python
def gmm_e_step(input, weights, means, variances) -> np.ndarray:
    """Returns shape (n_samples, k) responsibilities."""

def gmm_m_step(input, responsibilities) -> tuple[np.ndarray, np.ndarray, np.ndarray]:
    """Returns updated (weights, means, variances)."""
```

- Reuse `03-gaussian-naive-bayes`'s `gaussian_log_likelihood`.
- Diagonal covariance only, `variances[j]` is one number per feature, per component, no cross-feature covariance terms.

## Theory

`01-kmeans-assignment`/`02-kmeans-centroid-update` assign each point to exactly one cluster, a hard, all-or-nothing decision. A Gaussian Mixture Model (GMM) softens this: each cluster is a full Gaussian distribution (with its own mean, variance, and mixing weight), and a point gets a _probability_ of belonging to each cluster, not a single assignment.

This alternates two steps, structurally the same shape as K-Means's assign/update pair:

```text
1. E-step (Expectation, this question): given the current cluster parameters, compute
   how probable it is each point belongs to each cluster (the "responsibilities")
2. M-step (Maximization, this question): given those responsibilities, re-estimate
   each cluster's mean, variance, and mixing weight
   ... repeat (04-em-algorithm assembles the full loop)
```

The E-step is Bayes' rule again, the same shape `03-gaussian-naive-bayes`'s classification used: `responsibility[i,j] ∝ weight[j] * P(x_i | component j)`, normalized so each sample's responsibilities across all components sum to `1`. The only real difference from Naive Bayes classification is that there's no ground-truth label to check against, `responsibilities` themselves are the answer, a soft, probabilistic cluster assignment.

The M-step re-estimates each component's parameters as a _weighted_ average, weighted by how responsible that component is for each point: a component that's 90% responsible for a point counts it almost fully in its own mean/variance update, a component that's 5% responsible barely counts it at all. This is the direct generalization of `02-kmeans-centroid-update`'s plain average, K-Means is the special case of a GMM where every responsibility is either exactly `0` or exactly `1`.

## Explanation

`gmm_e_step` computes `log(weights[j]) + gaussian_log_likelihood(...)` for every sample-component pair (the log-space version of `weight * P(x|component)`, same reasoning `03-gaussian-naive-bayes` used to avoid tiny-probability underflow), then normalizes each row: `max_log` per row, subtracted before exponentiating (the standard log-sum-exp stability trick, keeps the largest exponentiated value at `exp(0)=1` instead of risking overflow), then divides by each row's sum so responsibilities are genuine probabilities.

`gmm_m_step`'s `effective_counts = responsibilities.sum(axis=0)` is how many samples "worth" of weight component `j` currently claims, a real number, not necessarily an integer, since responsibilities are fractional. `weights[j] = effective_counts[j] / n_samples` is that share of the whole dataset. `means[j]` is `responsibilities[:, j] @ input`, a weighted sum, divided by `effective_counts[j]`, the responsibility-weighted average position. `variances[j]` is the same weighted-average pattern applied to squared deviations from the new mean, per feature.
