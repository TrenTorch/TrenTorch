---
name: problem-193-greedy-decoding
title: 'Greedy Decoding'
tags: [problemset, transformer-llm, generation]
difficulty: Beginner
kind: problemset
relatedModule: 'part-language-modelling-attention-llms|Transformers'
topic: 'generation'
hint: 'argmax at every step'
tools: [NumPy]
---

## Statement

Return the index of the largest logit; ties select the first index.

Signature: `def solve(logits)`. Arguments are passed directly; return the stated value without printing.

### Example 1

```python
solve([0.1, 0.7, 0.2])
```

Returns:

```python
1
```

### Example 2

```python
solve([5.0, 1.0, 5.0])
```

Returns:

```python
0
```

## Theory

Greedy decoding uses argmax with first-occurrence tie resolution.

## Explanation

Return the index of the largest logit; ties select the first index. The examples show concrete inputs and expected returned values.
