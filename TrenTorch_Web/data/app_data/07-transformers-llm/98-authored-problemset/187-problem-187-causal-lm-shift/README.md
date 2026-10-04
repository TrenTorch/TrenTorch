---
name: problem-187-causal-lm-shift
title: "Causal LM Shift"
tags: [problemset, transformer-llm, pretraining-objectives]
difficulty: Intermediate
kind: problemset
relatedModule: "part-transformers-llm|Transformers"
topic: "pretraining objectives"
hint: "drop the last input token and first target token"
tools: [NumPy]
---

## Statement

Shift token IDs into next-token inputs and targets.

### Function signature

```python
def solve(ids):
```

Arguments are passed directly to `solve`; there is no stdin/stdout parsing. The function returns its result without printing.

### Examples

**Example 1**

**Input**

```python
solve([10, 11, 12, 13])
```

**Output**

```text
([10, 11, 12], [11, 12, 13])
```

**Example 2**

**Input**

```python
solve([7, 8])
```

**Output**

```text
([7], [8])
```

## Theory

### Core idea

Return all IDs except the last as inputs and all IDs except the first as next-token targets.

### Contract

The two output sequences overlap by one original token.

## Explanation

In Example 1, the stated operation produces the displayed result directly from the supplied inputs. Example 2 changes the input case while keeping the same rule, so it illustrates that the function applies the contract rather than special-casing one example.
