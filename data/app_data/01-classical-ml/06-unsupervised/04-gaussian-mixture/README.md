---
name: unsupervised-gaussian-mixture
title: Gaussian Mixture Clustering
tags: [classical-ml, unsupervised, clustering, gaussian-mixture]
difficulty: Advanced
---

## Statement

### The problem, from first principles

`01-kmeans-assignment` and `02-kmeans-centroid-update` cluster by making a hard call: every point belongs to exactly one centroid, full stop. That's fine when clusters are compact and well-separated, but it throws away real information when a point sits genuinely between two clusters — K-Means still forces a 100%/0% split on it, when 60%/40% would describe reality better.

A Gaussian Mixture Model keeps the same "clusters have centers" intuition but replaces each hard centroid with a full Gaussian distribution — its own mean, its own variance, and a mixing weight saying how much of the overall data it accounts for. A point no longer gets assigned to one cluster; it gets a _probability_ of having come from each one. That's the same probabilistic machinery `03-gaussian-naive-bayes` used to classify a point against known class distributions — the difference here is there are no known classes to check against, the "responsibilities" a point gets _are_ the answer.

### From theory to code

Implement `gmm_e_step(input, weights, means, variances)`, which computes each point's responsibility (posterior probability) under each component, and `gmm_m_step(input, responsibilities)`, which re-estimates each component's weight, mean, and variance from those responsibilities. Theory below shows the E-step is Bayes' rule reused from `03-gaussian-naive-bayes`, and the M-step is `02-kmeans-centroid-update`'s averaging generalized to fractional (soft) group membership instead of all-or-nothing membership.

### Constraints

- `input`: shape `(n_samples, n_features)`.
- `weights`: shape `(k,)`, mixing proportions, sum to 1.
- `means`: shape `(k, n_features)`.
- `variances`: shape `(k, n_features)` — diagonal covariance only, one variance per feature per component, no cross-feature covariance terms.
- `gmm_e_step` returns shape `(n_samples, k)`; every row must sum to exactly 1 (a genuine probability distribution over components).
- Reuse `03-gaussian-naive-bayes`'s `gaussian_log_likelihood`, don't recompute the Gaussian log-density by hand.
- `gmm_m_step` returns `(weights, means, variances)`, the same shapes as `gmm_e_step`'s inputs.
- Work in log-space and normalize with the row-max-subtraction trick before exponentiating — avoid underflow/overflow from raw probabilities.

### Hints

Open one at a time. Each gives away a little more than the last.

<details>
<summary>Hint 1</summary>

`weight[j] * P(x_i | component j)` is a product of tiny numbers. Working in log-space turns the product into `log(weight[j]) + gaussian_log_likelihood(...)`, a sum — compute that for every `(sample, component)` pair before doing anything else.

</details>

<details>
<summary>Hint 2</summary>

You can't exponentiate raw log-probabilities safely — they can be very negative, and `exp` of a very negative number underflows, but the real danger is the opposite: unnormalized values could differ enough to overflow before you divide. Subtract each row's max log-value before calling `np.exp`, then normalize by each row's sum. This doesn't change the final ratios, only the numerical stability of computing them.

</details>

<details>
<summary>Hint 3</summary>

For the M-step, `responsibilities[:, j].sum()` tells you how many samples' worth of "weight" component `j` currently claims — call it `effective_counts[j]`. Every other update for component `j` (weight, mean, variance) divides by this same number. The mean is a `responsibilities[:, j]`-weighted sum of `input`, divided by `effective_counts[j]`; when every responsibility is exactly 0 or 1 this collapses to `02-kmeans-centroid-update`'s plain group average.

</details>

## Theory

### The simple version

Instead of asking "which cluster's territory is this point standing in" (K-Means's hard boundary), ask "if I imagine each cluster as a fuzzy cloud with a center and a spread, how likely is it this particular cloud produced this particular point, relative to the other clouds?" A point near the middle of one cloud gets a high probability for that cloud and low probabilities for the others; a point sitting between two clouds gets a genuinely split probability, reflecting real ambiguity instead of forcing an arbitrary pick. K-Means is the special case of this where every cloud has collapsed to a single point and every probability has collapsed to exactly 0 or 1.

### The formula

E-step, for sample `i` and component `j` (in log-space for stability):

```
log_resp[i, j] = log(weights[j]) + gaussian_log_likelihood(input[i], means[j], variances[j])
responsibilities[i, :] = softmax(log_resp[i, :])   # exp(x - max(x)) / sum(exp(x - max(x)))
```

`gaussian_log_likelihood` sums the per-feature log-density (diagonal covariance means features are treated independently within a component).

M-step, given responsibilities:

```
effective_counts[j] = sum_i responsibilities[i, j]
weights[j]  = effective_counts[j] / n_samples
means[j]    = (sum_i responsibilities[i, j] * input[i]) / effective_counts[j]
variances[j][f] = (sum_i responsibilities[i, j] * (input[i, f] - means[j, f])**2) / effective_counts[j]
```

### How PyTorch actually implements this

There's no `torch.nn` GMM layer, but the two pieces here map onto real ops: the log-space normalization in the E-step is exactly what `torch.logsumexp` (subtract-max-then-log-sum-exp) is built to do stably, and the E/M alternation is a specific instance of the general Expectation-Maximization algorithm (assembled into a full loop in `05-em-algorithm`). No baked numeric oracle exists in `tests.py` for this question — the tests check hand-derivable properties (rows summing to 1, favoring the closer component, matching a plain average under hard responsibilities) rather than comparing to a specific external library's output.

## Explanation

`gmm_e_step` fills `log_responsibilities[i, j]` (solution.py lines 20-25) with `np.log(weights[j]) + gaussian_log_likelihood(input[i], means[j], variances[j])` for every sample-component pair — the log-space version of "prior times likelihood," the same reasoning `03-gaussian-naive-bayes` used to avoid multiplying many small probabilities together. `max_log = log_responsibilities.max(axis=1, keepdims=True)` (line 27) then `unnormalized = np.exp(log_responsibilities - max_log)` (line 28) is the stability trick: subtracting each row's max before exponentiating guarantees the largest term in that row becomes `exp(0) = 1`, so nothing overflows, and dividing by `max_log` doesn't change the final normalized ratios. `unnormalized / unnormalized.sum(axis=1, keepdims=True)` (line 29) turns that into a genuine per-row probability distribution — this is what `test_responsibilities_sum_to_one_per_sample` checks.

`gmm_m_step` computes `effective_counts = responsibilities.sum(axis=0)` (line 36) — how much total responsibility component `j` has claimed across all samples, a fractional number, not a count of hard assignments. `weights = effective_counts / n_samples` (line 38) is that share of the dataset. `means = (responsibilities.T @ input) / effective_counts[:, np.newaxis]` (line 39) computes, for every component at once, the responsibility-weighted sum of `input` (`responsibilities.T @ input` puts components on rows, features on columns) divided by that component's effective count — a weighted average, which `test_m_step_with_hard_responsibilities_matches_plain_kmeans_average` confirms collapses to `02-kmeans-centroid-update`'s plain average when responsibilities are exactly 0/1, and `test_m_step_uses_weighted_average_not_plain_average` confirms actually uses the weights rather than ignoring them. The `variances` loop (lines 42-44) repeats the same weighted-average pattern on squared deviations `diff = input - means[j]`, `(responsibilities[:, j] @ (diff**2)) / effective_counts[j]`, per feature, since `03-gaussian-naive-bayes`'s diagonal-covariance assumption means each feature's variance is estimated independently.
