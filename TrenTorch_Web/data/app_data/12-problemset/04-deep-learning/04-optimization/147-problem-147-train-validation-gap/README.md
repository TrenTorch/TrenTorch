---
name: problem-147-train-validation-gap
title: 'Train/Validation Gap'
tags: [problemset, dl-training-theory, generalization]
difficulty: Beginner
kind: problemset
relatedModule: 'part-deep-learning|Optimization'
topic: 'generalization'
hint: 'validation minus training'
tools: [NumPy]
---

## Statement

Compute the train/validation generalization gap.

### Function signature

```python
def solve(train_loss, val_loss):
```

Arguments are passed directly to `solve`; there is no stdin/stdout parsing. The function returns its result without printing.

### Examples

**Example 1**

**Input**

```python
solve(0.4, 0.6)
```

**Output**

```text
0.2
```

**Example 2**

**Input**

```python
solve(0.8, 0.7)
```

**Output**

```text
-0.1
```

## Theory

### Core idea

Subtract training loss from validation loss; a positive result means validation loss is higher.

### Contract

`gap = val_loss - train_loss`.

## Explanation

In Example 1, the stated operation produces the displayed result directly from the supplied inputs. Example 2 changes the input case while keeping the same rule, so it illustrates that the function applies the contract rather than special-casing one example.
