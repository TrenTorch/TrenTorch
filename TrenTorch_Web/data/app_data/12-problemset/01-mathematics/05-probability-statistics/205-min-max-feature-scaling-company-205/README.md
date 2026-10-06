---
name: min-max-feature-scaling-company-205
title: 'min-max-feature-scaling — AWS case'
tags: [problemset, data-stats-for-ds, data-cleaning, aws]
difficulty: Beginner
kind: problemset
relatedModule: 'part-mathematics|Probability & Statistics'
topic: 'Probability & Statistics'
caseCompany: 'AWS'
hint: 'Start from the mathematical definition and identify the one intermediate quantity that can be reused instead of recomputed.'
tools: [NumPy]
---

## Statement

AWS-inspired monitoring model combines numeric signals that arrive on very different scales. Before training, the team needs every feature mapped to a fixed interval, so you need to implement min-max scaling and handle the stated boundary cases correctly.

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
[10.0,20.0,30.0]
```

**Output**
```text
[0.0,0.5,1.0]
```

**Explanation:** The minimum maps to zero, the maximum to one, and the midpoint to one half.

### Hints

<details><summary>Hint 1</summary>
Start from the mathematical definition and identify the one intermediate quantity that can be reused instead of recomputed.
</details>

<details><summary>Hint 2</summary>
Pay attention to the boundary case in which the denominator, norm, mask, or candidate set can become degenerate.
</details>

## Theory

### The simple version

**min-max scaling** is the mechanism behind this task. The important idea is to implement the definition directly, while preserving numerical stability and the shape of the data that later stages expect.

### The formula

x'_i=(x_i-x_{min})/(x_{max}-x_{min}).

The symbols in the formula correspond directly to the values in the function signature; the implementation should compute these quantities in the same logical order.

### Worked reasoning

Min-max scaling preserves ordering while changing the numerical range.

## Explanation

The reference solution first converts inputs into the representation required by the operation, computes the necessary intermediate state once, and then returns the requested result. The key implementation choice is the handling of the non-obvious boundary or numerical case rather than merely reproducing the formula.

O(n) time and O(n) space.
