---
name: problem-180-transformer-residual-block
title: "Transformer Residual Block"
tags: [problemset, transformer-llm, transformer-architecture]
difficulty: Intermediate
kind: problemset
relatedModule: "part-transformers-llm|Transformers"
topic: "transformer architecture"
hint: "return x+sublayer(x)"
tools: [NumPy]
---

## Statement

Apply a residual connection around a callable sublayer.

### Function signature

```python
def solve(x, sublayer):
```

Arguments are passed directly to `solve`; there is no stdin/stdout parsing. The function returns its result without printing.

### Examples

**Example 1**

**Input**

```python
solve([1.0, 2.0], lambda values: values * 2)
```

**Output**

```text
[3.0, 6.0]
```

**Example 2**

**Input**

```python
solve([3.0, 4.0], lambda values: values * 0)
```

**Output**

```text
[3.0, 4.0]
```

## Theory

### Core idea

Evaluate the sublayer on `x` and add its output to `x` elementwise.

### Contract

`result = x + sublayer(x)`.

## Explanation

In Example 1, the stated operation produces the displayed result directly from the supplied inputs. Example 2 changes the input case while keeping the same rule, so it illustrates that the function applies the contract rather than special-casing one example.
