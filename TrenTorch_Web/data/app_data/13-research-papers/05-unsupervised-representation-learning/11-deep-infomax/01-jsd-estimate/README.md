---
name: research-dim-jsd-estimate
title: 'Deep InfoMax: The Jensen-Shannon MI Estimate'
tags: [research-papers, unsupervised, mutual-information, representation]
difficulty: Advanced
---

## Statement

### The problem, from first principles

Deep InfoMax (Hjelm et al., 2019) maximizes mutual information between an input's local features and its global summary, by training a discriminator to tell matched pairs from mismatched ones. The Jensen-Shannon form is a stable estimate built from softplus terms.

### From theory to code

Implement `jsd_estimate(pos, neg)`, the difference of the mean softplus terms over positive and negative pairs.

### Constraints

- Use `logaddexp(0, x)` for softplus.

### Hints

<details>
<summary>Hint 1</summary>

Positive pairs contribute `-softplus(-s)`, negative pairs contribute `-softplus(s)`.

</details>

## Theory

### The simple version

A discriminator that scores matched pairs high and mismatched pairs low makes this estimate large, which means the representation keeps information shared between local and global views.

### The formula

$$\hat I_{\text{JSD}} = \mathbb{E}_{P}\big[-\operatorname{sp}(-T(x,y))\big] - \mathbb{E}_{N}\big[\operatorname{sp}(T(x,y))\big], \quad \operatorname{sp}(u) = \log(1 + e^u)$$

### How NumPy/PyTorch actually implements this

The Deep InfoMax code computes the two softplus means from a batch of discriminator scores.

## Explanation

The estimate is a lower bound on mutual information, derived from the Jensen-Shannon divergence between joint and product distributions.
