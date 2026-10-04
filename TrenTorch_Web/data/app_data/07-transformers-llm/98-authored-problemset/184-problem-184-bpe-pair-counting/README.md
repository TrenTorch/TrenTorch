---
name: problem-184-bpe-pair-counting
title: "BPE Pair Counting"
tags: [problemset, transformer-llm, tokenization]
difficulty: Beginner
kind: problemset
relatedModule: "part-transformers-llm|NLP"
topic: "tokenization"
hint: "count adjacent pairs across token sequences"
tools: [NumPy]
---

## Statement

Find the most frequent adjacent token pair across a tokenized corpus.

### Function signature

```python
def solve(corpus):
```

Arguments are passed directly to `solve`; there is no stdin/stdout parsing. The function returns its result without printing.

### Examples

**Example 1**

**Input**

```python
solve([["a", "b", "a"], ["a", "b"]])
```

**Output**

```text
(('a', 'b'), 2)
```

**Example 2**

**Input**

```python
solve([["x", "y", "x", "y"]])
```

**Output**

```text
(('x', 'y'), 2)
```

## Theory

### Core idea

Count every adjacent pair within each sequence independently and return the highest-count pair with its frequency.

### Contract

Pairs do not cross sequence boundaries.

## Explanation

In Example 1, the stated operation produces the displayed result directly from the supplied inputs. Example 2 changes the input case while keeping the same rule, so it illustrates that the function applies the contract rather than special-casing one example.
