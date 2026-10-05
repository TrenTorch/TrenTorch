---
name: problem-200-benchmark-accuracy
title: 'Benchmark Accuracy'
tags: [problemset, transformer-llm, llm-evaluation]
difficulty: Intermediate
kind: problemset
relatedModule: 'part-language-modelling-attention-llms|Transformers'
topic: 'LLM evaluation'
hint: 'normalize only whitespace if specified'
tools: [NumPy]
---

## Statement

Return exact-match accuracy for paired strings after stripping outer whitespace. Matching is case-sensitive; sequences have equal nonzero length.

Signature: `def solve(predictions, targets)`. Arguments are passed directly; return the stated value without printing.

### Example 1

```python
solve(['cat', ' dog '], ['cat', 'dog'])
```

Returns:

```python
1.0
```

### Example 2

```python
solve(['A', 'b'], ['a', 'b'])
```

Returns:

```python
0.5
```

## Theory

Accuracy is the fraction of paired stripped strings that are identical.

## Explanation

Return exact-match accuracy for paired strings after stripping outer whitespace. Matching is case-sensitive; sequences have equal nonzero length. The examples show concrete inputs and expected returned values.
