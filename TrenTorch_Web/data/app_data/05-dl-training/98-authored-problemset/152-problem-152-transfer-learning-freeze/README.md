---
name: problem-152-transfer-learning-freeze
title: "Transfer Learning Freeze"
tags: [problemset, dl-training-theory, transfer-learning]
difficulty: Beginner
kind: problemset
relatedModule: "part-dl-training|Optimization"
topic: "transfer learning"
hint: "set requires_grad flags appropriately"
tools: [NumPy]
---

## Statement

Freeze backbone parameters and keep task-head parameters trainable.

### Function signature

```python
def solve(backbone, head):
```

Arguments are passed directly to `solve`; there is no stdin/stdout parsing. The function returns its result without printing.

### Examples

**Example 1**

**Input**

```python
solve([SimpleNamespace(requires_grad=True)], [SimpleNamespace(requires_grad=False)])
```

**Output**

```text
([namespace(requires_grad=False)], [namespace(requires_grad=True)])
```

**Example 2**

**Input**

```python
solve([SimpleNamespace(requires_grad=True), SimpleNamespace(requires_grad=True)], [SimpleNamespace(requires_grad=False)])
```

**Output**

```text
([namespace(requires_grad=False), namespace(requires_grad=False)], [namespace(requires_grad=True)])
```

## Theory

### Core idea

Set every backbone parameter’s `requires_grad` flag to false and every head parameter’s flag to true; return both parameter lists.

### Contract

Freezing changes gradient tracking, not the parameter values.

## Explanation

In Example 1, the stated operation produces the displayed result directly from the supplied inputs. Example 2 changes the input case while keeping the same rule, so it illustrates that the function applies the contract rather than special-casing one example.
