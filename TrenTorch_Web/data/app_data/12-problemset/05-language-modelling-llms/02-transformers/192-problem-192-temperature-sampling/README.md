---
name: problem-192-temperature-sampling
title: 'Temperature Sampling'
tags: [problemset, transformer-llm, generation]
difficulty: Advanced
kind: problemset
relatedModule: 'part-language-modelling-attention-llms|Transformers'
topic: 'generation'
hint: 'divide logits by temperature before softmax'
tools: [NumPy]
---

## Statement

Return softmax(logits / temperature) for positive temperature.

Signature: `def solve(logits, temperature)`. Arguments are passed directly; return the stated value without printing.

### Example 1

```python
solve([1.0, 2.0, 3.0], 1.0)
```

Returns:

```python
[0.09003057317038046, 0.24472847105479764, 0.6652409557748218]
```

### Example 2

```python
solve([0.0, 0.0], 1.0)
```

Returns:

```python
[0.5, 0.5]
```

## Theory

Subtract the maximum scaled logit before exponentiation and normalize exponentials to sum to one.

## Explanation

Return softmax(logits / temperature) for positive temperature. The examples show concrete inputs and expected returned values.
