---
name: problem-155-stable-logsumexp
title: "Stable LogSumExp"
tags: [problemset, dl-training-theory, numerical-stability]
difficulty: Intermediate
kind: problemset
relatedModule: "part-seq-modeling|Neural Networks"
topic: "numerical stability"
hint: "subtract max before exponentiating"
tools: [NumPy]
---

## Statement

Compute log-sum-exp without directly exponentiating large unshifted values.

### Function signature

```python
def solve(x):
```

Arguments are passed directly to `solve`; there is no stdin/stdout parsing. The function returns its result without printing.

### Examples

**Example 1**

**Input**

```python
solve([1000.0, 1001.0])
```

**Output**

```text
1001.31326169
```

**Example 2**

**Input**

```python
solve([0.0, 0.0])
```

**Output**

```text
0.69314718
```

## Theory

### Core idea

Subtract the maximum input before exponentiating, sum the exponentials, then add the maximum back.

### Contract

`logsumexp(x) = max(x) + log(sum(exp(x - max(x))))`.

## Explanation

In Example 1, the stated operation produces the displayed result directly from the supplied inputs. Example 2 changes the input case while keeping the same rule, so it illustrates that the function applies the contract rather than special-casing one example.
