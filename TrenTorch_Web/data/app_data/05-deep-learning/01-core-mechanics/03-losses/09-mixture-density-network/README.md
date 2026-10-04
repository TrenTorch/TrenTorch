---
name: dl-losses-mixture-density-network
title: Mixture Density Network Loss
tags: [deep-learning, losses, regression]
difficulty: Intermediate
---

## Statement

### The problem, from first principles

Mixture Density Network (MDN) loss is used when the target distribution is multimodal. Instead of predicting a single value, the model predicts a mixture of Gaussians.

For K components, the model outputs:
- pi_k: mixture weights (sum to 1)
- mu_k: means
- sigma_k: standard deviations

The loss is the negative log-likelihood:

$$\text{loss} = -\log\left(\sum_{k=1}^{K} \pi_k \mathcal{N}(y | \mu_k, \sigma_k^2)\right)$$

Where N is the Gaussian probability density.

### From theory to code

Implement:

```python
mdn_loss(y, pi, mu, sigma)
```

Where:
- y: targets (shape N,)
- pi: mixture weights (shape N, K)
- mu: means (shape N, K)
- sigma: standard deviations (shape N, K)

### Constraints

- All inputs must have compatible shapes.
- sigma > 0.
- sum(pi) = 1 for each sample.
- Return scalar loss.

## Theory

MDN loss marginalizes over mixture components, allowing the model to represent multimodal distributions.

## Explanation

For each sample, compute Gaussian PDF for each component, weight by pi, sum, take log, average over batch.
