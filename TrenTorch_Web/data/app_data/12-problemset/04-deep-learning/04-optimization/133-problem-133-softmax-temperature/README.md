---
name: problem-133-softmax-temperature
title: 'Softmax Temperature'
tags: [problemset, dl-core, attention---activations]
difficulty: Beginner
kind: problemset
relatedModule: 'part-deep-learning|Optimization'
topic: 'attention / activations'
hint: 'divide logits by positive temperature'
tools: [NumPy]
---

## Statement

Apply temperature scaling to logits and normalize them with softmax.

### Function signature

```python
def solve(logits, temperature):
```

Arguments are passed directly to `solve`; there is no stdin/stdout parsing. The function returns its result without printing.

### Examples

**Example 1**

**Input**

```python
solve([0.0, float(np.log(3.0))], 1.0)
```

**Output**

```text
[0.25, 0.75]
```

**Example 2**

**Input**

```python
solve([2.0, 2.0], 0.5)
```

**Output**

```text
[0.5, 0.5]
```

## Theory

### Core idea

Divide every logit by the positive temperature, subtract the largest scaled logit for numerical stability, then normalize exponentials.

### Contract

`p_i = exp(z_i / T) / Σ_j exp(z_j / T)`.

## Explanation

In Example 1, the stated operation produces the displayed result directly from the supplied inputs. Example 2 changes the input case while keeping the same rule, so it illustrates that the function applies the contract rather than special-casing one example.
