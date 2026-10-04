---
name: problem-197-prompt-token-budget
title: "Prompt Token Budget"
tags: [problemset, transformer-llm, prompting]
difficulty: Intermediate
kind: problemset
relatedModule: "part-transformers-llm|Transformers"
topic: "prompting"
hint: "subtract prompt length from context length"
tools: [NumPy]
---

## Statement

Return completion budget max(0, context_limit - prompt_tokens).

Signature: `def solve(context_limit, prompt_tokens)`. Arguments are passed directly; return the stated value without printing.

### Example 1

```python
solve(100, 35)
```

Returns:

```python
65
```

### Example 2

```python
solve(32, 40)
```

Returns:

```python
0
```

## Theory

The remaining context is floored at zero when prompt fills or exceeds the limit.

## Explanation

Return completion budget max(0, context_limit - prompt_tokens). The examples show concrete inputs and expected returned values.
