---
name: problem-149-random-search-sampler
title: 'Random Search Sampler'
tags: [problemset, dl-training-theory, hyperparameter-tuning]
difficulty: Intermediate
kind: problemset
relatedModule: 'part-deep-learning|Optimization'
topic: 'hyperparameter tuning'
hint: 'use seeded random sampling'
tools: [NumPy]
---

## Statement

Generate reproducible random-search configurations.

### Function signature

```python
def solve(n, seed=0):
```

Arguments are passed directly to `solve`; there is no stdin/stdout parsing. The function returns its result without printing.

### Examples

**Example 1**

**Input**

```python
solve(2, seed=0)
```

**Output**

```text
[{'lr': 0.0035305856304085927, 'depth': 6}, {'lr': 1.4584585665958855e-05, 'depth': 4}]
```

**Example 2**

**Input**

```python
solve(1, seed=7)
```

**Output**

```text
[{'lr': 0.0031650594102156206, 'depth': 7}]
```

## Theory

### Core idea

Use the supplied seed to draw learning rates log-uniformly from `1e-5` to `1e-1` and integer depths from 2 through 9.

### Contract

Each configuration contains an `lr` and a `depth`.

## Explanation

In Example 1, the stated operation produces the displayed result directly from the supplied inputs. Example 2 changes the input case while keeping the same rule, so it illustrates that the function applies the contract rather than special-casing one example.
