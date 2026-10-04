---
name: relu-layer-company-213
title: "relu-layer — OpenAI case"
tags: [problemset, dl-core, activation-functions, openai]
difficulty: Beginner
kind: problemset
relatedModule: "part-dl-training|Optimization"
topic: "Optimization"
caseCompany: "OpenAI"
hint: "Start from the mathematical definition and identify the one intermediate quantity that can be reused instead of recomputed."
tools: [NumPy]
---

## Statement

Apply ReLU elementwise, returning max(x,0) at every position.

Signature: `def solve(x)`. Arguments are passed directly; return the stated value without printing.

### Example 1

```python
solve([-2.0, 0.0, 3.0])
```

Returns:

```python
[0.0, 0.0, 3.0]
```

### Example 2

```python
solve([0.0])
```

Returns:

```python
[0.0]
```

## Theory

ReLU(x)=max(0,x), suppressing negative values and preserving nonnegative values.

## Explanation

Apply ReLU elementwise, returning max(x,0) at every position. The examples show concrete inputs and expected returned values.
