---
name: gini-impurity-company-208
title: 'gini-impurity — Cloudflare case'
tags: [problemset, classical-ml-trees-ensembles, decision-trees, cloudflare]
difficulty: Beginner
kind: problemset
relatedModule: 'part-classical-ml|Classification'
topic: 'Classification'
caseCompany: 'Cloudflare'
hint: 'Start from the mathematical definition and identify the one intermediate quantity that can be reused instead of recomputed.'
tools: [NumPy]
---

## Statement

Return binary-label Gini impurity; empty sequence has impurity 0.0.

Signature: `def solve(y)`. Arguments are passed directly; return the stated value without printing.

### Example 1

```python
solve([1, 1, 0, 0])
```

Returns:

```python
0.5
```

### Example 2

```python
solve([])
```

Returns:

```python
0.0
```

## Theory

For p=fraction of label 1, impurity is 1-p²-(1-p)².

## Explanation

Return binary-label Gini impurity; empty sequence has impurity 0.0. The examples show concrete inputs and expected returned values.
