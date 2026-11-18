---
name: research-lottery-magnitude-mask
title: 'The Lottery Ticket Hypothesis: Magnitude Pruning Mask'
tags: [research-papers, classical-ml, pruning, lottery-ticket]
difficulty: Intermediate
---

## Statement

### The problem, from first principles

Frankle & Carbin (2019) found that a sparse subnetwork, chosen by pruning the smallest-magnitude weights after training, can train to the same accuracy as the full network from its original initialization. The first step is choosing which weights to keep.

### From theory to code

Implement `magnitude_mask(w, keep_fraction)`, which keeps the largest-magnitude weights and returns a boolean mask.

### Constraints

- Keep `ceil(keep_fraction * size)` weights.

### Hints

<details>
<summary>Hint 1</summary>

Sort the absolute values in descending order, mark the top `k` as True, and reshape to the weights' shape.

</details>

## Theory

### The simple version

Large weights carry most of the signal, so pruning the small ones removes the least function. The mask then defines the sparse network the paper retrains from its original initialization.

### The formula

$$m_i = \mathbb{1}\big[\,|w_i| \text{ is among the } \lceil k\,n\rceil \text{ largest}\,\big]$$

### How NumPy/PyTorch actually implements this

Pruning libraries build the same boolean mask from `torch.topk` on absolute weights.

## Explanation

The argsort gives the ranking; the mask marks the top entries, matching the one-shot pruning step in the paper.
