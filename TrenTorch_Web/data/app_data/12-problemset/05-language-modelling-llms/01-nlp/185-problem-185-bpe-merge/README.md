---
name: problem-185-bpe-merge
title: 'BPE Merge'
tags: [problemset, transformer-llm, tokenization]
difficulty: Intermediate
kind: problemset
relatedModule: 'part-language-modelling-attention-llms|NLP'
topic: 'tokenization'
hint: 'scan each token sequence once'
tools: [NumPy]
---

## Statement

Merge non-overlapping occurrences of one adjacent token pair.

### Function signature

```python
def solve(seq, pair):
```

Arguments are passed directly to `solve`; there is no stdin/stdout parsing. The function returns its result without printing.

### Examples

**Example 1**

**Input**

```python
solve(["a", "b", "a", "b", "c"], ("a", "b"))
```

**Output**

```text
['ab', 'ab', 'c']
```

**Example 2**

**Input**

```python
solve(["a", "x", "b"], ("a", "b"))
```

**Output**

```text
['a', 'x', 'b']
```

## Theory

### Core idea

Scan left to right; replace matching adjacent elements with their concatenation and consume both elements before continuing.

### Contract

Non-matching elements are copied unchanged.

## Explanation

In Example 1, the stated operation produces the displayed result directly from the supplied inputs. Example 2 changes the input case while keeping the same rule, so it illustrates that the function applies the contract rather than special-casing one example.
