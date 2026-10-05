---
name: problem-199-rlhf-reward-normalization
title: 'RLHF Reward Normalization'
tags: [problemset, transformer-llm, rlhf-intuition]
difficulty: Intermediate
kind: problemset
relatedModule: 'part-language-modelling-attention-llms|Transformers'
topic: 'RLHF intuition'
hint: 'standardize reward values'
tools: [NumPy]
---

## Statement

Return reward z-scores using population std: (rewards-mean)/std; rewards must not be constant.

Signature: `def solve(rewards)`. Arguments are passed directly; return the stated value without printing.

### Example 1

```python
solve([1.0, 2.0, 3.0])
```

Returns:

```python
[-1.224744871391589, 0.0, 1.224744871391589]
```

### Example 2

```python
solve([-3.0, -2.0, -1.0])
```

Returns:

```python
[-1.224744871391589, 0.0, 1.224744871391589]
```

## Theory

Subtract population mean and divide by population standard deviation (ddof=0).

## Explanation

Return reward z-scores using population std: (rewards-mean)/std; rewards must not be constant. The examples show concrete inputs and expected returned values.
