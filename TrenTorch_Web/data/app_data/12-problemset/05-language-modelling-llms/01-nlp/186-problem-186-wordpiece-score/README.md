---
name: problem-186-wordpiece-score
title: 'WordPiece Score'
tags: [problemset, transformer-llm, tokenization]
difficulty: Intermediate
kind: problemset
relatedModule: 'part-language-modelling-attention-llms|NLP'
topic: 'tokenization'
hint: 'use pair_count/(left_count*right_count)'
tools: [NumPy]
---

## Statement

Compute the WordPiece pair score from occurrence counts.

### Function signature

```python
def solve(pair_count, left_count, right_count):
```

Arguments are passed directly to `solve`; there is no stdin/stdout parsing. The function returns its result without printing.

### Examples

**Example 1**

**Input**

```python
solve(2, 4, 5)
```

**Output**

```text
0.1
```

**Example 2**

**Input**

```python
solve(3, 2, 5)
```

**Output**

```text
0.3
```

## Theory

### Core idea

Divide the pair count by the product of the left-token and right-token counts.

### Contract

`score = pair_count / (left_count * right_count)`.

## Explanation

In Example 1, the stated operation produces the displayed result directly from the supplied inputs. Example 2 changes the input case while keeping the same rule, so it illustrates that the function applies the contract rather than special-casing one example.
