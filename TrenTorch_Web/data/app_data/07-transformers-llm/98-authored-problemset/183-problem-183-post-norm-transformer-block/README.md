---
name: problem-183-post-norm-transformer-block
title: "Post-Norm Transformer Block"
tags: [problemset, transformer-llm, layer-norm-and-residuals]
difficulty: Beginner
kind: problemset
relatedModule: "part-transformers-llm|Transformers"
topic: "layer norm and residuals"
hint: "use post-norm ordering"
tools: [NumPy]
---

## Statement

Apply a post-norm transformer block with attention and feed-forward residuals.

### Function signature

```python
def solve(x, norm, attention, ff):
```

Arguments are passed directly to `solve`; there is no stdin/stdout parsing. The function returns its result without printing.

### Examples

**Example 1**

**Input**

```python
solve([1.0, 2.0], lambda v: np.asarray(v) * 2, lambda v: np.asarray(v) + 1, lambda v: np.asarray(v) * 0.5)
```

**Output**

```text
[12.0, 20.0]
```

**Example 2**

**Input**

```python
solve([1.0, 1.0], lambda v: np.asarray(v), lambda v: np.zeros_like(v), lambda v: np.zeros_like(v))
```

**Output**

```text
[2.0, 2.0]
```

## Theory

### Core idea

Run attention on the unnormalized input, normalize after its residual addition, then run feed-forward and normalize after the second residual.

### Contract

`z = norm(x + attention(x))`; `out = norm(z + ff(z))`.

## Explanation

In Example 1, the stated operation produces the displayed result directly from the supplied inputs. Example 2 changes the input case while keeping the same rule, so it illustrates that the function applies the contract rather than special-casing one example.
