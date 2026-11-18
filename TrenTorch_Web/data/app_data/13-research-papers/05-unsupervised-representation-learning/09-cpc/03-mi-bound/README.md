---
name: research-cpc-mi-bound
title: 'CPC: The Mutual Information Bound'
tags: [research-papers, unsupervised, predictive-coding, contrastive]
difficulty: Beginner
---

## Statement

### The problem, from first principles

The CPC paper shows that the loss bounds the mutual information between context and future from below. The bound equals log N minus the loss, so a better classifier gives a tighter bound on the information it captures.

### From theory to code

Implement `mi_lower_bound(n_candidates, loss)`, returning `log(N) - loss`.

### Constraints

- Returns a Python float.

### Hints

<details>
<summary>Hint 1</summary>

Compute the natural log of the candidate count and subtract the loss.

</details>

## Theory

### The simple version

The bound cannot exceed log N, the information in the choice among N candidates. A loss close to zero means the model identifies the true future almost every time.

### The formula

$$I(x; c) \ge \log N - \mathcal{L}_N$$

### How NumPy/PyTorch actually implements this

Evaluation scripts report this estimate alongside the loss as a measure of how much the representation knows.

## Explanation

The bound grows with N, so larger candidate sets allow tighter estimates of the information the encoder captures.
