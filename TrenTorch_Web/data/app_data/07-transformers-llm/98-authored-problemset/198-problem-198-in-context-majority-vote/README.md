---
name: problem-198-in-context-majority-vote
title: "In-Context Majority Vote"
tags: [problemset, transformer-llm, in-context-learning]
difficulty: Intermediate
kind: problemset
relatedModule: "part-transformers-llm|Transformers"
topic: "in-context learning"
hint: "count labels in the demonstrations"
tools: [NumPy]
---

## Statement

Return most frequent label; ties resolve to first label in sorted unique-value order.

Signature: `def solve(labels)`. Arguments are passed directly; return the stated value without printing.

### Example 1

```python
solve([1, 2, 1, 3, 1])
```

Returns:

```python
1
```

### Example 2

```python
solve([2, 1, 2, 1])
```

Returns:

```python
1
```

## Theory

Count unique labels, select greatest count, and resolve ties by sorted order.

## Explanation

Return most frequent label; ties resolve to first label in sorted unique-value order. The examples show concrete inputs and expected returned values.
