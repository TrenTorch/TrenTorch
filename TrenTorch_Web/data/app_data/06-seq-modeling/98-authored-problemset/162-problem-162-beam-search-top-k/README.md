---
name: problem-162-beam-search-top-k
title: "Beam Search Top-K"
tags: [problemset, sequence-models-attention, beam-search]
difficulty: Advanced
kind: problemset
relatedModule: "part-seq-modeling|Neural Networks"
topic: "beam search"
hint: "expand candidates then sort by cumulative score"
tools: [NumPy]
---

## Statement

Keep the top `k` cumulative-score sequences after expanding each beam step.

### Function signature

```python
def solve(step_scores, k):
```

Arguments are passed directly to `solve`; there is no stdin/stdout parsing. The function returns its result without printing.

### Examples

**Example 1**

**Input**

```python
solve([[0.0, -1.0], [-2.0, 0.0]], 2)
```

**Output**

```text
[([0, 1], 0.0), ([1, 1], -1.0)]
```

**Example 2**

**Input**

```python
solve([[-1.0, 0.5, 0.0]], 1)
```

**Output**

```text
[([1], 0.5)]
```

## Theory

### Core idea

Append every token choice, add its step score to the beam score, sort by descending total score with deterministic sequence ordering for ties, and keep `k`.

### Contract

Scores are summed across steps; no softmax is applied.

## Explanation

In Example 1, the stated operation produces the displayed result directly from the supplied inputs. Example 2 changes the input case while keeping the same rule, so it illustrates that the function applies the contract rather than special-casing one example.
