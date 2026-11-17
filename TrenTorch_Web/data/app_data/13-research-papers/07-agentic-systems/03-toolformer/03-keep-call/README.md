---
name: research-toolformer-keep-call
title: 'Toolformer: Keeping Useful Calls'
tags: [research-papers, agents, tool-use, toolformer]
difficulty: Intermediate
---

## Statement

### The problem, from first principles

Toolformer keeps an inserted call only if it helps. The model's loss on the following words is computed with and without the call and its result, and the call survives only if the loss drops by a margin tau.

### From theory to code

Implement `keep_call(loss_without, loss_with, tau)`, returning whether the call is kept.

### Constraints

- Returns a bool; the threshold is inclusive.

### Hints

<details>
<summary>Hint 1</summary>

Compute the reduction `loss_without - loss_with` and compare it with `tau`.

</details>

## Theory

### The simple version

Filtering by loss keeps only calls that actually inform the model. Calls that do not change the prediction are removed, so the model is not taught to call tools needlessly.

### The formula

$$\text{keep} \iff L(\text{no call}) - L(\text{call}) \ge \tau$$

### How NumPy/PyTorch actually implements this

The paper's self-supervised pipeline applies this filter to every candidate call before fine-tuning.

## Explanation

The filter uses the model's own likelihoods, so the training data is self-generated and self-filtered.
