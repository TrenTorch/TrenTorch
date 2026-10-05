---
name: problem-177-unknown-token-mapping
title: 'Unknown Token Mapping'
tags: [problemset, sequence-models-attention, tokenization]
difficulty: Beginner
kind: problemset
relatedModule: 'part-language-modelling-attention-llms|NLP'
topic: 'tokenization'
hint: 'dictionary lookup with default'
tools: [NumPy]
---

## Statement

Map tokens to vocabulary IDs, using `unk_id` for missing tokens.

### Function signature

```python
def solve(tokens, vocab, unk_id):
```

Arguments are passed directly to `solve`; there is no stdin/stdout parsing. The function returns its result without printing.

### Examples

**Example 1**

**Input**

```python
solve(["a", "z", "b"], {"a": 2, "b": 5}, 0)
```

**Output**

```text
[2, 0, 5]
```

**Example 2**

**Input**

```python
solve(["x", "x"], {"x": 9}, -1)
```

**Output**

```text
[9, 9]
```

## Theory

### Core idea

Look up each token independently and preserve input order.

### Contract

The output has one ID for every input token.

## Explanation

In Example 1, the stated operation produces the displayed result directly from the supplied inputs. Example 2 changes the input case while keeping the same rule, so it illustrates that the function applies the contract rather than special-casing one example.
