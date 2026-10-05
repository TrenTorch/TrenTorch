---
name: problem-166-causal-mask
title: 'Causal Mask'
tags: [problemset, sequence-models-attention, attention-mechanism]
difficulty: Beginner
kind: problemset
relatedModule: 'part-language-modelling-attention-llms|Transformers'
topic: 'attention mechanism'
hint: 'use indices i>=j'
tools: [NumPy]
---

## Statement

Construct the lower-triangular causal attention mask.

### Function signature

```python
def solve(n):
```

Arguments are passed directly to `solve`; there is no stdin/stdout parsing. The function returns its result without printing.

### Examples

**Example 1**

**Input**

```python
solve(3)
```

**Output**

```text
[[True, False, False], [True, True, False], [True, True, True]]
```

**Example 2**

**Input**

```python
solve(1)
```

**Output**

```text
[[True]]
```

## Theory

### Core idea

Position `i` may attend to key positions `j <= i`.

### Contract

The output is a boolean square matrix of size `n`.

## Explanation

In Example 1, the stated operation produces the displayed result directly from the supplied inputs. Example 2 changes the input case while keeping the same rule, so it illustrates that the function applies the contract rather than special-casing one example.
