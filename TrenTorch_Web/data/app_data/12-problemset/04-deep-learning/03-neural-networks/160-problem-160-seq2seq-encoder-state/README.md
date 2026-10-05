---
name: problem-160-seq2seq-encoder-state
title: 'Seq2Seq Encoder State'
tags: [problemset, sequence-models-attention, seq2seq]
difficulty: Intermediate
kind: problemset
relatedModule: 'part-deep-learning|Neural Networks'
topic: 'seq2seq'
hint: 'iterate through the sequence'
tools: [NumPy]
---

## Statement

Return the final hidden state produced by a sequence encoder.

### Function signature

```python
def solve(X, h0, Wx, Wh, b):
```

Arguments are passed directly to `solve`; there is no stdin/stdout parsing. The function returns its result without printing.

### Examples

**Example 1**

**Input**

```python
solve([[1.0], [2.0]], [0.0], [[1.0]], [[0.5]], [0.0])
```

**Output**

```text
[0.9830411]
```

**Example 2**

**Input**

```python
solve([[0.0], [0.0]], [1.0], [[1.0]], [[0.0]], [0.0])
```

**Output**

```text
[0.0]
```

## Theory

### Core idea

Initialize with `h0`, apply the tanh RNN update for every row of `X`, and return only the final state.

### Contract

Unlike sequence-forward output, this representation contains no time axis.

## Explanation

In Example 1, the stated operation produces the displayed result directly from the supplied inputs. Example 2 changes the input case while keeping the same rule, so it illustrates that the function applies the contract rather than special-casing one example.
