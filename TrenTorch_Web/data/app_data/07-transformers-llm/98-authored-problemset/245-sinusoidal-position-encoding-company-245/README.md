---
name: sinusoidal-position-encoding-company-245
title: "sinusoidal-position-encoding — Amazon case"
tags: [problemset, transformer-llm, positional-encoding-intro, amazon]
difficulty: Intermediate
kind: problemset
relatedModule: "part-transformers-llm|Transformers"
topic: "Transformers"
caseCompany: "Amazon"
hint: "Start from the mathematical definition and identify the one intermediate quantity that can be reused instead of recomputed."
tools: [NumPy]
---

## Statement

Amazon-inspired sequence model needs deterministic position information without adding learned position parameters. You need to construct the sinusoidal positional encoding for the requested sequence length and embedding dimension.

### Input Format

```python
solve(n, d)
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
solve(1, 1)
```

**Output**
```text
[[0.0]]
```

The output is produced by running the reference solution with these arguments.

**Example 2**

**Input**
```python
solve(1, 1)
```

**Output**
```text
[[0.0]]
```

The output is produced by running the reference solution with these arguments.

### Hints

<details><summary>Hint</summary>

Start from the mathematical definition and identify the one intermediate quantity that can be reused instead of recomputed.

</details>

## Theory

### The simple version

**positional encoding** is the mechanism behind this task. The important idea is to implement the definition directly, while preserving numerical stability and the shape of the data that later stages expect.

### The formula

PE_{pos,2i}=sin(pos/10000^{2i/d}), PE_{pos,2i+1}=cos(pos/10000^{2i/d}).

The symbols in the formula correspond directly to the values in the function signature; the implementation should compute these quantities in the same logical order.

### Worked reasoning

Sinusoidal encodings inject position using deterministic functions whose frequencies vary across dimensions.

## Explanation

The reference solution first converts inputs into the representation required by the operation, computes the necessary intermediate state once, and then returns the requested result. The key implementation choice is the handling of the non-obvious boundary or numerical case rather than merely reproducing the formula.

O(nd) time and O(nd) space.
