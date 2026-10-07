---
name: problem-153-fine-tuning-lr-groups
title: 'Fine-Tuning LR Groups'
tags: [problemset, dl-training-theory, fine-tuning]
difficulty: Intermediate
kind: problemset
relatedModule: 'part-deep-learning|Optimization'
topic: 'fine tuning'
hint: 'two dicts: backbone with lr*factor, head with lr'
tools: [NumPy]
---

## Statement

Build two optimiser parameter groups for fine-tuning: the backbone gets the learning rate `base_lr * backbone_factor` and the head gets `base_lr`.

Implement `solve(backbone, head, base_lr, backbone_factor)`.

**Returns.** Return `[{'params': list(backbone), 'lr': base_lr * backbone_factor}, {'params': list(head), 'lr': base_lr}]`.

### Examples

**Example 1**

Input:

```python
solve(['backbone'], ['head'], 0.1, 0.1)
```

Output:

```text
[{'params': ['backbone'], 'lr': 0.01}, {'params': ['head'], 'lr': 0.1}]
```

**Example 2**

Input:

```python
solve([], ['head'], 0.01, 0.2)
```

Output:

```text
[{'params': [], 'lr': 0.002}, {'params': ['head'], 'lr': 0.01}]
```

## Theory

### The simple version

When fine-tuning, the pre-trained backbone should change gently so its good features survive, while the freshly initialised head must learn quickly. Optimisers accept _parameter groups_, each with its own learning rate, so both needs can be met in one optimiser.

### The setup

$$\eta_{\text{backbone}}=\eta\cdot\rho,\qquad \eta_{\text{head}}=\eta,\qquad \rho<1$$

## Explanation

A factor of $0.1$ makes the backbone learn ten times slower than the head. The returned list has the structure PyTorch optimisers expect, e.g. `torch.optim.AdamW(groups)`.
