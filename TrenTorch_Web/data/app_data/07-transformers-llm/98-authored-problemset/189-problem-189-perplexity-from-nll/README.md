---
name: problem-189-perplexity-from-nll
title: "Perplexity from NLL"
tags: [problemset, transformer-llm, llm-evaluation]
difficulty: Advanced
kind: problemset
relatedModule: "part-transformers-llm|Transformers"
topic: "LLM evaluation"
hint: "return exp(mean_nll)"
tools: [NumPy]
---

## Statement

Return scalar perplexity exp(mean_nll).

Signature: `def solve(mean_nll)`. Arguments are passed directly; return the stated value without printing.

### Example 1

```python
solve(0.5)
```

Returns:

```python
1.6487212707001282
```

### Example 2

```python
solve(0.0)
```

Returns:

```python
1.0
```

## Theory

Exponentiating mean negative log-likelihood converts it to perplexity.

## Explanation

Return scalar perplexity exp(mean_nll). The examples show concrete inputs and expected returned values.
