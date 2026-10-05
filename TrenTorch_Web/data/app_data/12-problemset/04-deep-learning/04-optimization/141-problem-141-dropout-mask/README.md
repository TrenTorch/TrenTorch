---
name: problem-141-dropout-mask
title: 'Dropout Mask'
tags: [problemset, dl-training-theory, regularization]
difficulty: Advanced
kind: problemset
relatedModule: 'part-deep-learning|Optimization'
topic: 'regularization'
hint: 'sample Bernoulli mask and divide by keep probability'
tools: [NumPy]
---

## Statement

Apply seeded inverted dropout to an activation array.

### Function signature

```python
def solve(x, keep_prob, seed=0):
```

Arguments are passed directly to `solve`; there is no stdin/stdout parsing. The function returns its result without printing.

### Examples

**Example 1**

**Input**

```python
solve([1.0, 2.0, 3.0, 4.0], 0.5, 0)
```

**Output**

```text
[0.0, 4.0, 6.0, 8.0]
```

**Example 2**

**Input**

```python
solve([1.0, 2.0, 3.0, 4.0], 1.0, 7)
```

**Output**

```text
[1.0, 2.0, 3.0, 4.0]
```

## Theory

### Core idea

Draw a Bernoulli keep mask from `seed`, zero dropped activations, and scale retained values by `1 / keep_prob`.

### Contract

The mask makes the expectation of each output activation equal to its input activation.

## Explanation

In Example 1, the stated operation produces the displayed result directly from the supplied inputs. Example 2 changes the input case while keeping the same rule, so it illustrates that the function applies the contract rather than special-casing one example.
