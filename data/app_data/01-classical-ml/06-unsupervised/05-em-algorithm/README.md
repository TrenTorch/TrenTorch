---
name: unsupervised-em-algorithm
title: 'Stretch: EM Algorithm'
tags: [classical-ml, unsupervised, clustering, gaussian-mixture, stretch]
difficulty: Advanced
---

## Statement

Implement:

```python
def gmm_log_likelihood(input, weights, means, variances) -> float: ...
def fit_gmm(input, n_components, max_iter, seed=None) -> dict: ...
```

- Reuse `04-gaussian-mixture`'s `gmm_e_step`/`gmm_m_step`, don't reimplement either.

## Theory

`04-gaussian-mixture` built the two individual steps. This question assembles them into the actual **Expectation-Maximization (EM)** algorithm, the same "primitive first, then the full loop" pattern `03-best-split-minimal-tree` (search, then recursion) and `04-full-boosting-loop` (one round, then the loop) already established.

EM has a real mathematical guarantee that most iterative algorithms in this curriculum don't state outright: **each E-step/M-step pair can only increase (or leave unchanged) the data's total log-likelihood under the model, never decrease it.** Gradient descent needs a small enough learning rate to guarantee this kind of steady improvement, EM guarantees it by construction, every iteration is a provably-non-decreasing step toward a local maximum of the likelihood.

```text
initialize weights, means, variances (e.g. random data points as starting means)
repeat max_iter times:
    E-step: compute responsibilities given current parameters
    M-step: re-estimate parameters given those responsibilities
    (log-likelihood after this iteration >= log-likelihood before it, always)
```

Total log-likelihood, `sum over samples of log(sum over components of weight * P(x|component))`, is the actual quantity EM is climbing. Tracking it every iteration isn't just for a progress bar, it's how you'd notice a real implementation bug: if it ever decreases, something in the E-step or M-step is wrong, this is a genuinely strong correctness check, not just a nice-to-have.

## Explanation

`gmm_log_likelihood` builds the same `log(weight) + gaussian_log_likelihood(...)` matrix `gmm_e_step` builds, but instead of normalizing each row into a probability distribution (responsibilities), it needs `log(sum of the row's un-logged values)`, computed stably: subtract each row's max before exponentiating (log-sum-exp), sum, take the log, add the max back. Summing that stable per-sample value across every sample gives the total log-likelihood.

`fit_gmm` initializes by picking `n_components` distinct training rows (via `rng.choice(..., replace=False)`) as starting means, a common, simple GMM initialization, uniform starting weights, and every component starting with the same overall data variance (a neutral starting guess, refined once real E/M iterations begin). The loop is exactly `04-gaussian-mixture`'s two functions, called in sequence, `max_iter` times, recording `gmm_log_likelihood` after each M-step into `log_likelihood_history`, the sequence Theory says must never decrease.
