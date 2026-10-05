---
name: semi-supervised-e-step
title: 'Semi-supervised E-step for a Gaussian mixture'
tags: [classical-ml, semi-supervised, em, gaussian-mixture, log-sum-exp]
difficulty: Intermediate
---

## Statement

### Responsibilities for a Gaussian mixture, with labeled points clamped

In semi-supervised EM for a Gaussian mixture, the E-step computes each point's responsibility for each component. Labeled points are not allowed to move: their responsibility is one-hot on their known class.

Implement two functions.

- `responsibilities(X, means, covs, priors)` returns an `(N, K)` array. Row `i` gives `p(component k | x_i)` under the mixture. Compute it in log space with log-sum-exp so that far-away points give finite values.
- `semi_supervised_e_step(X, y, means, covs, priors)` takes `y` with `-1` for unlabeled points and class indices `0..K-1` for labeled ones. It returns the same `(N, K)` array, with labeled rows replaced by one-hot vectors.

### Constraints

- `X` is 2-D, `means` is `(K, d)`, `covs` is `(K, d, d)`, `priors` is `(K,)`.
- Each covariance must be symmetric positive definite. Priors must be strictly positive and sum to 1.
- Shape mismatches raise `ValueError`. So does a label outside `-1..K-1`.
- Rows of the output sum to 1.
- Do not modify the inputs.

### Hints

<details>
<summary>Hint 1</summary>

Compute `log p(x | k) + log pi_k` for every component, then subtract the row maximum before exponentiating.

</details>

## Theory

EM alternates between responsibilities (E-step) and parameter updates (M-step). With labels, the E-step is clamped: a labeled point contributes its label as fact, not as a probabilistic guess. This is the main reason semi-supervised EM can beat plain supervised training on small labeled sets, and also the reason it can go badly wrong when the mixture assumption is false, since a wrong model then reinforces its own mistakes on the unlabeled data.

### Where this shows up in production

Gaussian mixtures with a few hand-labeled examples show up in fraud and quality-control pipelines, where a labeling team marks a small number of cases and the rest of the stream is unlabeled. Log-space responsibilities are what keeps these systems from producing `NaN` when a transaction is far from every cluster, which happens in real data all the time.

### Using it to make decisions

Use this when your features really are close to a Gaussian per class and labels are scarce. Check the assumption first: plot the labeled classes and confirm they look elliptical. If they do not, a graph-based or self-training method usually does better. Compare against a supervised baseline on the labeled points alone, and only keep the semi-supervised model if the held-out labeled error improves.

### Pros and cons

**Pros:** principled probabilities, a clean way to use unlabeled data, and a closed-form E-step with no tuning beyond the model.

**Cons:** a wrong Gaussian assumption amplifies errors, EM finds local optima that depend on initialization, and covariance estimates are fragile with few points per class.

## Explanation

The responsibilities are computed as normalized exponentials of log joint terms. Subtracting the row maximum keeps the largest term at zero so the exponential cannot underflow to a row of zeros. The semi-supervised step then overwrites the labeled rows with one-hot vectors, which is the clamping step.
