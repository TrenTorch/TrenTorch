---
name: problem-153-fine-tuning-lr-groups
title: 'Fine-Tuning LR Groups'
tags: [problemset, dl-training-theory, fine-tuning]
difficulty: Intermediate
kind: problemset
relatedModule: 'part-deep-learning|Optimization'
topic: 'fine tuning'
hint: 'construct parameter groups'
tools: [NumPy]
---

## Statement

Build two optimizer parameter groups for fine-tuning.

### Function signature

```python
def solve(backbone, head, base_lr, backbone_factor):
```

Arguments are passed directly to `solve`; there is no stdin/stdout parsing. The function returns its result without printing.

### Examples

**Example 1**

**Input**

```python
solve(["backbone"], ["head"], 0.1, 0.1)
```

**Output**

```text
[{'params': ['backbone'], 'lr': 0.01}, {'params': ['head'], 'lr': 0.1}]
```

**Example 2**

**Input**

```python
solve([], ["head"], 0.01, 0.2)
```

**Output**

```text
[{'params': [], 'lr': 0.002}, {'params': ['head'], 'lr': 0.01}]
```

## Theory

### Core idea

Scale the backbone learning rate by `backbone_factor`; the head receives `base_lr`.

### Contract

The returned groups pair each original parameter collection with its assigned rate.

## Explanation

In Example 1, the stated operation produces the displayed result directly from the supplied inputs. Example 2 changes the input case while keeping the same rule, so it illustrates that the function applies the contract rather than special-casing one example.
