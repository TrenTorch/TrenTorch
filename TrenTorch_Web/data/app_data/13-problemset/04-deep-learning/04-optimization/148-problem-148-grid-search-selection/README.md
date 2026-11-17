---
name: problem-148-grid-search-selection
title: 'Grid Search Selection'
tags: [problemset, dl-training-theory, hyperparameter-tuning]
difficulty: Beginner
kind: problemset
relatedModule: 'part-deep-learning|Optimization'
topic: 'hyperparameter tuning'
hint: 'min(results, key=(val_loss, str(params))), None if empty'
tools: [NumPy]
---

## Statement

Pick the best result of a grid search. `results` is a list of dicts with a `val_loss` and a `params` entry; return the record with the lowest validation loss. Ties are broken by the smaller `str(params)`, and an empty list returns `None`.

Implement `solve(results)`.

**Returns.** Return the winning record (the same dict object), or `None` for an empty input.

### Examples

**Example 1**

Input:

```python
solve([{'val_loss': 0.8, 'params': {'lr': 0.1}}, {'val_loss': 0.5, 'params': {'lr': 0.01}}])
```

Output:

```text
{'val_loss': 0.5, 'params': {'lr': 0.01}}
```

**Example 2**

Input:

```python
solve([{'val_loss': 0.5, 'params': {'lr': 0.1}}, {'val_loss': 0.5, 'params': {'lr': 0.01}}])
```

Output:

```text
{'val_loss': 0.5, 'params': {'lr': 0.01}}
```

## Theory

### The simple version

Grid search tries every combination from a small list of hyper-parameter values, scores each one on a validation set, and keeps the best. It is simple and exhaustive, but the number of combinations grows exponentially with the number of hyper-parameters.

### The selection rule

$$\theta^*=\arg\min_{\theta\in\text{grid}}L_{\text{val}}(\theta)$$

### Why it matters

- Grid search tries every combination from a small list of settings and keeps the one that does best, which makes tuning systematic and reproducible.
- Choosing by validation loss (never test loss) keeps the final test score honest.

### How it works

1. Compare the `val_loss` of every record.
2. Return the record with the lowest value.
3. If two tie, the smaller `str(params)` wins; an empty list gives `None`.

### Worked example

The two records have validation losses $0.8$ (learning rate $0.1$) and $0.5$ (learning rate $0.01$). The lower one wins, so the result is {'val_loss': 0.5, 'params': {'lr': 0.01}}.

## Explanation

Equal losses (second example) need a deterministic tie-break so the same input always gives the same answer; here the textual form of the parameters decides, which prefers `{'lr': 0.01}` over `{'lr': 0.1}` because the character `'0'` sorts before `'1'`. The selection must use the _validation_ loss, never the test loss.
