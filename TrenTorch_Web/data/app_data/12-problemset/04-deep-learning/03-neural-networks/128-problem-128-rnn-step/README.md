---
name: problem-128-rnn-step
title: 'RNN Step'
tags: [problemset, dl-core, rnn-basics]
difficulty: Intermediate
kind: problemset
relatedModule: 'part-deep-learning|Neural Networks'
topic: 'rnn basics'
hint: 'h=tanh(Wx+Uh_prev+b)'
tools: [NumPy]
---

## Statement

A vanilla RNN step updates one hidden vector from the current input and previous state.

### Function signature

```python
def solve(x, h, Wx, Wh, b):
```

Arguments are passed directly to `solve`; there is no stdin/stdout parsing. The function returns its result without printing.

### Examples

**Example 1**

**Input**

```python
solve([1.0, 2.0], [0.0, 1.0], [[1.0, 0.0], [0.0, 1.0]], [[1.0, 0.0], [0.0, 1.0]], [0.0, 0.0])
```

**Output**

```text
[0.76159416, 0.99505475]
```

**Example 2**

**Input**

```python
solve([0.0, 0.0], [0.0, 0.0], [[1.0, 0.0], [0.0, 1.0]], [[1.0, 0.0], [0.0, 1.0]], [1.0, -1.0])
```

**Output**

```text
[0.76159416, -0.76159416]
```

## Theory

### Core idea

Apply the affine input and recurrent transforms, add the bias, then pass the result through `tanh`.

### Contract

`h_next = tanh(Wx @ x + Wh @ h + b)`.

## Explanation

In Example 1, the stated operation produces the displayed result directly from the supplied inputs. Example 2 changes the input case while keeping the same rule, so it illustrates that the function applies the contract rather than special-casing one example.
