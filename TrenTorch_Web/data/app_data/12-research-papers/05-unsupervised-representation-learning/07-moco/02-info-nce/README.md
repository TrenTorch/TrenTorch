---
name: research-moco-info-nce
title: 'MoCo: The InfoNCE Loss With a Queue'
tags: [research-papers, unsupervised, contrastive, momentum]
difficulty: Advanced
---

## Statement

### The problem, from first principles

MoCo trains the query to pick its positive key out of a large queue of negative keys. The loss is InfoNCE: a softmax over normalized similarities, scaled by a temperature.

### From theory to code

Implement `info_nce(q, k_pos, negatives, tau)`, normalizing the query and keys, then computing the softmax loss of the positive.

### Constraints

- Normalize every vector before computing similarities.

### Hints

<details>
<summary>Hint 1</summary>

Normalize the query and all keys, compute scaled dot products, then use `logsumexp` minus the positive logit.

</details>

## Theory

### The simple version

The loss rewards a query for matching its own key more than the queue. A large queue provides many negatives, which the momentum encoder keeps consistent.

### The formula

$$\mathcal{L}_q = -\log\frac{\exp(q \cdot k_+/\tau)}{\exp(q \cdot k_+/\tau) + \sum_{i=1}^{K}\exp(q \cdot k_i/\tau)}$$

### How NumPy/PyTorch actually implements this

MoCo's training loop calls a cross-entropy over the positive and queue logits, the same computation.

## Explanation

The normalization makes the loss invariant to the scale of the features, which is why a scale change of the query leaves it unchanged.
