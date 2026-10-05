---
name: problem-148-grid-search-selection
title: 'Grid Search Selection'
tags: [problemset, dl-training-theory, hyperparameter-tuning]
difficulty: Beginner
kind: problemset
relatedModule: 'part-deep-learning|Optimization'
topic: 'hyperparameter tuning'
hint: 'deterministic lexicographic tie-break'
tools: [NumPy]
---

## Statement

Select the grid-search result with the lowest validation loss.

### Function signature

```python
def solve(results):
```

Arguments are passed directly to `solve`; there is no stdin/stdout parsing. The function returns its result without printing.

### Examples

**Example 1**

**Input**

```python
solve([{"val_loss": 0.8, "params": {"lr": 0.1}}, {"val_loss": 0.5, "params": {"lr": 0.01}}])
```

**Output**

```text
{'val_loss': 0.5, 'params': {'lr': 0.01}}
```

**Example 2**

**Input**

```python
solve([{"val_loss": 0.5, "params": {"lr": 0.1}}, {"val_loss": 0.5, "params": {"lr": 0.01}}])
```

**Output**

```text
{'val_loss': 0.5, 'params': {'lr': 0.01}}
```

## Theory

### Core idea

Choose the record with smallest `val_loss`; for ties, compare the string representations of `params` for deterministic selection.

### Contract

Return the original winning result record.

## Explanation

In Example 1, the stated operation produces the displayed result directly from the supplied inputs. Example 2 changes the input case while keeping the same rule, so it illustrates that the function applies the contract rather than special-casing one example.
