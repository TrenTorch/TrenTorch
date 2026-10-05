---
name: problem-188-masked-lm-labels
title: 'Masked LM Labels'
tags: [problemset, transformer-llm, pretraining-objectives]
difficulty: Intermediate
kind: problemset
relatedModule: 'part-language-modelling-attention-llms|Transformers'
topic: 'pretraining objectives'
hint: 'use ignore index elsewhere'
tools: [NumPy]
---

## Statement

Return ids and same-shaped labels: true mask positions contain the token ID; all other labels contain ignore_index (default -100).

Signature: `def solve(ids, mask, ignore_index=-100)`. Arguments are passed directly; return the stated value without printing.

### Example 1

```python
solve([101, 205, 7], [True, False, True], -100)
```

Returns:

```python
[[101, 205, 7], [101, -100, 7]]
```

### Example 2

```python
solve([8, 9], [False, True], -1)
```

Returns:

```python
[[8, 9], [-1, 9]]
```

## Theory

label[j] is ids[j] when mask[j] is true, otherwise ignore_index.

## Explanation

Return ids and same-shaped labels: true mask positions contain the token ID; all other labels contain ignore_index (default -100). The examples show concrete inputs and expected returned values.
