---
name: problem-152-transfer-learning-freeze
title: 'Transfer Learning Freeze'
tags: [problemset, dl-training-theory, transfer-learning]
difficulty: Beginner
kind: problemset
relatedModule: 'part-deep-learning|Optimization'
topic: 'transfer learning'
hint: 'loop: backbone params requires_grad=False, head params requires_grad=True'
tools: [NumPy]
---

## Statement

Prepare a model for transfer learning: set `requires_grad = False` on every backbone parameter and `requires_grad = True` on every task-head parameter. The parameter objects are modified in place.

Implement `solve(backbone, head)`.

**Returns.** Return a tuple `(backbone_list, head_list)` containing the same parameter objects as lists.

### Examples

**Example 1**

Input:

```python
solve([SimpleNamespace(requires_grad=True)], [SimpleNamespace(requires_grad=False)])
```

Output:

```text
([namespace(requires_grad=False)], [namespace(requires_grad=True)])
```

**Example 2**

Input:

```python
solve([], [SimpleNamespace(requires_grad=False), SimpleNamespace(requires_grad=False)])
```

Output:

```text
([], [namespace(requires_grad=True), namespace(requires_grad=True)])
```

## Theory

### The simple version

A network pre-trained on a large dataset already contains useful general features. For a new task with little data you can keep those features fixed (freeze the backbone) and train only a small new output layer (the head). That is faster, needs less data and avoids destroying what the backbone already knows.

### What freezing means

A parameter with `requires_grad = False` receives no gradient, so the optimiser never changes it.

## Explanation

The function simply flips the flag on each object, which is exactly what PyTorch does for real `Parameter` tensors. Freezing the head would leave the model unable to learn the new task, so the head is explicitly set trainable. An empty backbone is allowed.
