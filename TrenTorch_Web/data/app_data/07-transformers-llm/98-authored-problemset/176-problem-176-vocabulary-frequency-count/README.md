---
name: problem-176-vocabulary-frequency-count
title: "Vocabulary Frequency Count"
tags: [problemset, sequence-models-attention, sequence-modeling]
difficulty: Beginner
kind: problemset
relatedModule: "part-transformers-llm|Transformers"
topic: "sequence modeling"
hint: "use a dictionary or Counter"
tools: [NumPy]
---

## Statement

Return the `k` most frequent vocabulary tokens and their counts.

### Function signature

```python
def solve(tokens, k):
```

Arguments are passed directly to `solve`; there is no stdin/stdout parsing. The function returns its result without printing.

### Examples

**Example 1**

**Input**

```python
solve(["a", "b", "a", "c", "b", "a"], 2)
```

**Output**

```text
[('a', 3), ('b', 2)]
```

**Example 2**

**Input**

```python
solve(["x", "y", "x"], 1)
```

**Output**

```text
[('x', 2)]
```

## Theory

### Core idea

Count token occurrences, sort by descending frequency, and preserve first-seen order for ties.

### Contract

The result is a list of `(token, count)` pairs.

## Explanation

In Example 1, the stated operation produces the displayed result directly from the supplied inputs. Example 2 changes the input case while keeping the same rule, so it illustrates that the function applies the contract rather than special-casing one example.
