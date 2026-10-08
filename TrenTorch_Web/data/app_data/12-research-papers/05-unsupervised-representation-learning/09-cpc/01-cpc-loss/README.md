---
name: research-cpc-loss
title: 'CPC: The Contrastive Loss'
tags: [research-papers, unsupervised, predictive-coding, contrastive]
difficulty: Intermediate
---

## Statement

### The problem, from first principles

Contrastive Predictive Coding (van den Oord et al., 2018) predicts future latent codes from the present context. Among many candidate futures, the true one should get the highest score, which is a softmax classification problem.

### From theory to code

Implement `cpc_loss(scores, pos)`, the softmax cross-entropy of the true future among the candidates.

### Constraints

- Use `logsumexp` for stability.

### Hints

<details>
<summary>Hint 1</summary>

Compute `logsumexp(scores) - scores[pos]`.

</details>

## Theory

### The simple version

The loss is a lower bound on the mutual information between context and future, and it gets tighter with more candidates. Predicting the future forces the encoder to keep the information that matters.

### The formula

$$\mathcal{L}_N = -\mathbb{E}\left[\log\frac{\exp(s(x_{t+k}, c_t))}{\sum_{j}\exp(s(x_j, c_t))}\right]$$

### How NumPy/PyTorch actually implements this

CPC implementations compute the score matrix for a batch and call `cross_entropy` with the diagonal as targets.

## Explanation

The expression is a categorical cross-entropy over the candidate set, with the true future as the target class.
