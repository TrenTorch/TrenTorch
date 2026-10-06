---
name: sinusoidal-position-encoding-company-245
title: 'sinusoidal-position-encoding — Amazon case'
tags: [problemset, transformer-llm, positional-encoding-intro, amazon]
difficulty: Intermediate
kind: problemset
relatedModule: 'part-language-modelling-attention-llms|Transformers'
topic: 'Transformers'
caseCompany: 'Amazon'
hint: 'Start from the mathematical definition and identify the one intermediate quantity that can be reused instead of recomputed.'
tools: [NumPy]
---

## Statement

Amazon-inspired sequence model needs deterministic position information without adding learned position parameters. You need to construct the sinusoidal positional encoding for the requested sequence length and embedding dimension.

### Input Format

```text
See the `solve(...)` signature in the reference implementation. Arguments are ordinary Python values or NumPy arrays; no stdin/stdout parsing is used.
```

### Output Format

```text
Return exactly the scalar, vector, matrix, tuple, or other Python object described by the statement.
```

### Constraints

- Inputs must satisfy the dimensions and value assumptions stated by the problem.
- Use finite floating-point values unless the statement explicitly permits another case.
- Input sizes are bounded so the reference implementation completes comfortably within the platform limit.
- Time limit: 20 seconds (platform default — see processes/code-execution/pyodide-service.ts).

### Example

**Input**

```text
2,4
```

**Output**

```text
[[0,1,0,1],[0.84147098,0.54030231,0.00999983,0.99995]]
```

**Explanation:** Position zero produces zeros for sine channels and ones for cosine channels.

### Hints

<details><summary>Hint 1</summary>
Start from the mathematical definition and identify the one intermediate quantity that can be reused instead of recomputed.
</details>

<details><summary>Hint 2</summary>
Pay attention to the boundary case in which the denominator, norm, mask, or candidate set can become degenerate.
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
