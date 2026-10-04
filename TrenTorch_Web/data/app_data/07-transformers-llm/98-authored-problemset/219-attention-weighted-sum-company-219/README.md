---
name: attention-weighted-sum-company-219
title: "attention-weighted-sum — Swiggy case"
tags: [problemset, sequence-models-attention, attention-mechanism, swiggy]
difficulty: Beginner
kind: problemset
relatedModule: "part-transformers-llm|Transformers"
topic: "Transformers"
caseCompany: "Swiggy"
hint: "Start from the mathematical definition and identify the one intermediate quantity that can be reused instead of recomputed."
tools: [NumPy]
---

## Statement

Swiggy-inspired recommendation model combines several encoded signals using learned attention weights. You need to compute the weighted sum correctly so the model produces the intended context representation.

### Input Format

```python
solve(scores, V)
```

Arguments are passed directly to the function; there is no stdin/stdout parsing.

### Output Format

Return the value computed by `solve`; do not print it.

### Constraints

- Inputs must satisfy the dimensions and value assumptions stated by the problem.
- Use finite floating-point values unless the statement explicitly permits another case.
- Input sizes are bounded so the reference implementation completes comfortably within the platform limit.

- Time limit: 20 seconds (platform default — see processes/code-execution/pyodide-service.ts).

### Example

**Example 1**

**Input**
```python
solve(...)
```

**Output**
```text
See the function's return value for this input.
```

The output is produced by running the reference solution with these arguments.

### Hints

<details><summary>Hint</summary>

Start from the mathematical definition and identify the one intermediate quantity that can be reused instead of recomputed.

</details>

## Theory

### The simple version

**attention** is the mechanism behind this task. The important idea is to implement the definition directly, while preserving numerical stability and the shape of the data that later stages expect.

### The formula

a_i=softmax(s)_i,\quad y=\sum_i a_i v_i.

The symbols in the formula correspond directly to the values in the function signature; the implementation should compute these quantities in the same logical order.

### Worked reasoning

Attention turns pairwise relevance scores into a convex combination of value vectors.

## Explanation

The reference solution first converts inputs into the representation required by the operation, computes the necessary intermediate state once, and then returns the requested result. The key implementation choice is the handling of the non-obvious boundary or numerical case rather than merely reproducing the formula.

O(nd) time and O(n) temporary space.
