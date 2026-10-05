---
name: problem-182-pre-norm-transformer-block
title: 'Pre-Norm Transformer Block'
tags: [problemset, transformer-llm, layer-norm-and-residuals]
difficulty: Advanced
kind: problemset
relatedModule: 'part-language-modelling-attention-llms|Transformers'
topic: 'layer norm and residuals'
hint: 'use pre-norm residual structure'
tools: [NumPy]
---

## Statement

Apply a pre-norm transformer block with attention and feed-forward residuals.

### Function signature

```python
def solve(x, norm, attention, ff):
```

Arguments are passed directly to `solve`; there is no stdin/stdout parsing. The function returns its result without printing.

### Examples

**Example 1**

**Input**

```python
solve([1.0, 2.0], lambda v: np.asarray(v) * 2, lambda v: np.asarray(v) + 1, lambda v: np.asarray(v) * 0.5)
```

**Output**

```text
[8.0, 14.0]
```

**Example 2**

**Input**

```python
solve([1.0, 1.0], lambda v: np.asarray(v), lambda v: np.zeros_like(v), lambda v: np.zeros_like(v))
```

**Output**

```text
[1.0, 1.0]
```

## Theory

### Core idea

Normalize before attention, add the attention result to `x`, normalize that intermediate state, then add the feed-forward output.

### Contract

`z = x + attention(norm(x))`; `out = z + ff(norm(z))`.

## Explanation

In Example 1, the stated operation produces the displayed result directly from the supplied inputs. Example 2 changes the input case while keeping the same rule, so it illustrates that the function applies the contract rather than special-casing one example.
